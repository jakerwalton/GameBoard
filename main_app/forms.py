from django.forms import ModelForm
from .models import Achievements

class AchievementForm(ModelForm):
  class Meta:
    model = Achievements
    fields = ['date', 'achievement']