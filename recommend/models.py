from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator 

import uuid as uuid_lib

# Create your models here.
class Anime(models.Model):
    anime_id = models.IntegerField(primary_key=True, editable=False)
    name = models.CharField(max_length=50, null=True, blank=True)
    genre = models.CharField(max_length=50, null=True, blank=True)
    anime_type = models.CharField(max_length=50, null=True, blank=True)
    episodes = models.IntegerField(validators=[MinValueValidator(0)], null=True, blank=True)
    anime_rating = models.FloatField(validators=[MinValueValidator(0.0), MaxValueValidator(10.0)], null=True, blank=True)
    members = models.IntegerField(validators=[MinValueValidator(0)], null=True, blank=True)

    def __unicode__(self):
        return self.anime_id

class Rating(models.Model):
    #id = models.UUIDField(default=uuid_lib.uuid4, primary_key=True, editable=False)
    user_id = models.CharField(max_length=50)
    anime_id = models.ForeignKey(Anime, on_delete=models.SET_NULL, null=True)
    evaluation = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(10)])

    def __unicode__(self):
        return self.anime_id

class Result(models.Model):
    #id = models.UUIDField(default=uuid_lib.uuid4, primary_key=True, editable=False)
    user_id = models.CharField(max_length=50)
    anime_id = models.ForeignKey(Anime, on_delete=models.SET_NULL, null=True)
    evaluation = models.FloatField(validators=[MinValueValidator(0.0), MaxValueValidator(10.0)])

    def __unicode__(self):
        return self.anime_id

class ResultKNN(models.Model):
    rating_id = models.UUIDField(default=uuid_lib.uuid4, primary_key=True, editable=False)
    user_id = models.CharField(max_length=50)
    anime_id = models.ForeignKey(Anime, on_delete=models.SET_NULL, null=True)
    evaluation = models.FloatField(validators=[MinValueValidator(0.0), MaxValueValidator(10.0)])

    def __unicode__(self):
        return self.rating_id