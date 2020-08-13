from django import forms
from .models import Anime, Rating

class AnimeForm(forms.ModelForm):
  class Meta:
    model = Anime
    fields = ('name', 'genre', 'anime_type', 'episodes')

class RatingForm(forms.ModelForm):
  class Meta:
    model = Rating
    fields = ('evaluation',)