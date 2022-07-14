from django.shortcuts import render, redirect
from django.views.generic import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

from main_app.forms import AchievementForm
from .models import Game, Platform, Photo

import uuid
import boto3


S3_BASE_URL = 'https://s3.us-east-1.amazonaws.com/'
BUCKET = 'catcollecter-jakew-1'





def home(request):
    return render(request, 'home.html')

def about(request):
  return render(request, 'about.html')

@login_required
def games_index(request):
    games = Game.objects.filter(user=request.user)
    return render(request, 'games/index.html', {'games': games})

@login_required
def games_detail(request, game_id):
    game = Game.objects.get(id=game_id)
    available_platforms = Platform.objects.exclude(
        id__in = game.platforms.all().values_list('id'))
    achievement_form = AchievementForm()
    return render(request, 'games/detail.html', {
        'game': game,
        'achievement_form': achievement_form,
        'platforms': available_platforms
    })

@login_required
def add_achievement(request, game_id):
    form = AchievementForm(request.POST)
    if form.is_valid():
        new_achievement = form.save(commit=False)
        new_achievement.game_id = game_id
        new_achievement.save()
    return redirect('detail', game_id=game_id)

@login_required
def assoc_platform(request, game_id, platform_id):
    Game.objects.get(id=game_id).platforms.add(platform_id)
    return redirect('detail', game_id=game_id)

@login_required
def assoc_platform_delete(request, game_id, platform_id):
    Game.objects.get(id=game_id).platforms.remove(platform_id)
    return redirect('detail', game_id=game_id)

@login_required
def add_photo(request, game_id):
    photo_file = request.FILES.get('photo-file', None)
    if photo_file:
        s3 = boto3.client('s3')
        key = uuid.uuid4().hex[:6] + photo_file.name[photo_file.name.rfind('.'):]
        try:
            s3.upload_fileobj(photo_file, BUCKET, key)
            url = f"{S3_BASE_URL}{BUCKET}/{key}"
            photo = Photo(url=url, game_id=game_id)
            photo.save()
        except:
            print('An error occurred uploading file to S3')
    return redirect('detail', game_id=game_id)

def signup(request):
    error_message = ''
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('index')
        else:
            error_message = 'Invalid sign up - try again'
    form = UserCreationForm()
    context = {'form':form, 'error_message':error_message}
    return render(request, 'registration/signup.html', context)



class GameCreate(LoginRequiredMixin, CreateView):
    model = Game
    fields = ['name', 'developer', 'coverart']
    success_url = '/games/'
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

class GameUpdate(LoginRequiredMixin, UpdateView):
    model = Game
    fields = ['name', 'developer']

class GameDelete(LoginRequiredMixin, DeleteView):
    model = Game
    success_url = '/games/'

class PlatformList(LoginRequiredMixin, ListView):
    model = Platform
    template_name = 'platforms/index.html'

class PlatformDetail(LoginRequiredMixin, DetailView):
    model = Platform
    template_name = 'platforms/detail.html'

class PlatformCreate(LoginRequiredMixin, CreateView):
    model = Platform
    fields = ['name']
    success_url = '/platforms/'

class PlatformUpdate(LoginRequiredMixin, UpdateView):
    model = Platform
    fields = '__all__'

class PlatformDelete(LoginRequiredMixin, DeleteView):
    model = Platform
    success_url = '/platforms/'