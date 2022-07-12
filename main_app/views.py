from django.shortcuts import render, redirect
from django.views.generic import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from main_app.forms import AchievementForm

from .models import Game, Platform

def home(request):
    return render(request, 'home.html')

def about(request):
  return render(request, 'about.html')

def games_index(request):
    games = Game.objects.all()
    return render(request, 'games/index.html', {'games': games})

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

def add_achievement(request, game_id):
    form = AchievementForm(request.POST)
    if form.is_valid():
        new_achievement = form.save(commit=False)
        new_achievement.game_id = game_id
        new_achievement.save()
    return redirect('detail', game_id=game_id)

def assoc_platform(request, game_id, platform_id):
    Game.objects.get(id=game_id).platforms.add(platform_id)
    return redirect('detail', game_id=game_id)

def assoc_platform_delete(request, game_id, platform_id):
    Game.objects.get(id=game_id).platforms.remove(platform_id)
    return redirect('detail', game_id=game_id)

class Games:
    def __init__(self, name, developer):
        self.name = name
        self.developer = developer

class GameCreate(CreateView):
    model = Game
    fields = ['name', 'developer']
    success_url = '/games/'

class GameUpdate(UpdateView):
    model = Game
    fields = ['name', 'developer']

class GameDelete(DeleteView):
    model = Game
    success_url = '/games/'

class PlatformList(ListView):
    model = Platform
    template_name = 'platforms/index.html'

class PlatformDetail(DetailView):
    model = Platform
    template_name = 'platforms/detail.html'

class PlatformCreate(CreateView):
    model = Platform
    fields = ['name']
    success_url = '/platforms/'

class PlatformUpdate(UpdateView):
    model = Platform
    fields = '__all__'

class PlatformDelete(DeleteView):
    model = Platform
    success_url = '/platforms/'