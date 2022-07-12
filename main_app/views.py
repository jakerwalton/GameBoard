from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView
from django.views.generic.detail import DetailView
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm  
# from .models import Cat, Toy, Photo
# from .forms import FeedingForm
import uuid
# import boto3

def home(request):
    return render(request, 'home.html')

def about(request):
  return render(request, 'about.html')

def games_index(request):
    return render(request, 'games/index.html', {'games'})