from django.contrib import admin
from recommend.models import Result, Anime, Rating

# Register your models here.
admin.site.register(Result)
admin.site.register(Anime)
admin.site.register(Rating)