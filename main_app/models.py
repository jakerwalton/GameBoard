from django.db import models
from django.urls import reverse
from datetime import date
from django.contrib.auth.models import User



class Platform(models.Model):
    name = models.CharField(max_length=50)

class Game(models.Model):
    name = models.CharField(max_length=100)
    developer = models.CharField(max_length=100)
    platforms = models.ManyToManyField(Platform)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('detail', kwargs={'game_id': self.id})

class Achievements(models.Model):
    date = models.DateField('Date Earned')
    achievement = models.CharField(max_length=100)

    game = models.ForeignKey(Game, on_delete=models.CASCADE)

    def __str__(self):
        return f'"{self.achievement}" earned on {self.date}'
    class Meta:
        ordering = ['-date']


class Photo(models.Model):
    url = models.CharField(max_length=200)
    game = models.ForeignKey(Game, on_delete=models.CASCADE)

    def __str__(self):
        return f"Photo for game_id: {self.game_id} @{self.url}"