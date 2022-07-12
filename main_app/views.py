from django.shortcuts import render, redirect
from django.views.generic import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from main_app.forms import AchievementForm

from .models import Game

def home(request):
    return render(request, 'home.html')

def about(request):
  return render(request, 'about.html')

def games_index(request):
    games = Game.objects.all()
    return render(request, 'games/index.html', {'games': games})

def games_detail(request, game_id):
    game = Game.objects.get(id=game_id)
    achievement_form = AchievementForm()
    return render(request, 'games/detail.html', { 
        'game': game,
        'achievement_form': achievement_form,
    })

def add_achievement(request, game_id):
        form = AchievementForm(request.POST)
        if form.is_valid():
            new_achievement = form.save(commit=False)
            new_achievement.game_id = game_id
            new_achievement.save()
        return redirect('detail', game_id=game_id)

class Games:
    def __init__(self, name, developer):
        self.name = name
        self.developer = developer

class GameCreate(CreateView):
    model = Game
    fields = '__all__'
    success_url = '/games/'

class GameUpdate(UpdateView):
    model = Game
    fields = '__all__'

class GameDelete(DeleteView):
    model = Game
    success_url = '/games/'