from django.core.management.base import BaseCommand
from django.utils import timezone
import json, sys
import pandas as pd
from recommend.models import Anime

class Command(BaseCommand):
    help = 'Displays current time'

    def handle(self, *args, **kwargs):
        time = timezone.now().strftime('%X')
        self.stdout.write("It's now %s" % time)

        Anime.objects.all().delete()

        df = pd.read_csv("static/recommend/anime.csv")

        for _, row in df.iterrows():
            hh = Anime()

            hh.anime_id = row[0]
            hh.name = row[1]
            if row[2] is not None:
                hh.genre = row[2]
            else:
                hh.genre = "None"
            hh.anime_type = row[3]
            if row.episodes == "Unknown":
                row.episodes = -1
            hh.episodes = row[4]    
            hh.anime_rating = row[5]
            hh.members = row[6]

            hh.save()