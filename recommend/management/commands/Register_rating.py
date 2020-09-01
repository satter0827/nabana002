from django.core.management.base import BaseCommand
from django.utils import timezone
import json, sys
import pandas as pd
from recommend.models import Rating, Anime

class Command(BaseCommand):
    help = 'Displays current time'
    max_count = 100

    def handle(self, *args, **kwargs):
        time = timezone.now().strftime('%X')
        self.stdout.write("It's now %s" % time)

        Rating.objects.all().delete()

        df = pd.read_csv("static/recommend/rating.csv",encoding='cp932')

        count = 0

        for _, row in df.iterrows():
            if row[0] >= self.max_count:
                break

            count+=1

            if count % 1000 == 0:
                print(row[0])

            if row[2] == -1:
                continue

            hh = Rating()

            hh.user_id = row[0]

            if Anime.objects.filter(anime_id=int(row[1])):
                hh.anime_id = Anime.objects.get(anime_id=int(row[1]))
            else:
                continue

            hh.evaluation = row[2]
            
            hh.save()

