from django.core.management.base import BaseCommand
from django.utils import timezone
from django_pandas.io import read_frame
from django.conf import settings
from collections import defaultdict
from surprise import SVD, SVDpp,KNNBasic
from surprise import Reader, Dataset

import json, sys
import pandas as pd

from recommend.models import Anime, Rating, Result

class Command(BaseCommand):
  help = 'Displays current time'

  def get_top_n(self, predictions, n=10):
    top_n = defaultdict(list)
    for uid, iid, _, est, _ in predictions:
      top_n[uid].append((iid, est))

    # そして各ユーザに対して予測値をソートして最も高いk個を返す。
    for uid, user_ratings in top_n.items():
      user_ratings.sort(key=lambda x: x[1], reverse=True)
      top_n[uid] = user_ratings[:n]

    return top_n

  def handle(self, *args, **kwargs):
    time = timezone.now().strftime('%X')
    self.stdout.write("It's now %s" % time)

    count = Rating.objects.count()
    min = 0
    max = 999

    df = pd.DataFrame(index=[], columns=["user_id", "anime_id", "evaluation"])

    while min < count:
      rating_temp = Rating.objects.values_list('pk', flat=True)[min:max]
      df_temp = read_frame(rating_temp, fieldnames=["user_id", "anime_id", "evaluation"])
      df = df.append(df_temp)

      min = max
      max = max + 1000

      if count < max:
        max = count

    df['anime_id'] = df['anime_id'].str.replace("Anime object \(", '')
    df['anime_id'] = df['anime_id'].str.replace(')', '')

    print("done : read rating table")

    # まずmovielensデータセットでSVDアルゴリズムを学習させる。
    #reader = Reader(line_format='user item rating', sep=',', rating_scale=(1, 10))
    #data = Dataset.load_from_file("static/recommend/rating.csv", reader=reader)

    reader = Reader(rating_scale=(1, 10))
    data = Dataset.load_from_df(df[['user_id', 'anime_id', 'evaluation']], reader=reader)

    trainset = data.build_full_trainset()

    sim_options = {
    'name': 'pearson', # 類似度を計算する方法を指定（ cosine,msd,pearson,pearson_baseline ）
    'user_based': True # False にするとアイテムベースに
    }

    algo = SVD()
    #algo = SVDpp()
    #algo = KNNBasic(k=5, min_k=1,sim_options=sim_options)
    algo.fit(trainset)

    # そして学習用データに含まれていない全ての（ユーザ、アイテムの）組み合わせに対して評価を予測する。
    testset = trainset.build_anti_testset()
    predictions = algo.test(testset)

    top_n = self.get_top_n(predictions, n=10)

    print("done : make result")

    Result.objects.all().delete()

    for key in top_n:
      unit = top_n[key]
      for item in unit:
        result = Result()
        result.user_id = key
        if len(key) != 36:
          continue
        if Anime.objects.filter(anime_id=int(item[0])):
            result.anime_id = Anime.objects.get(anime_id=int(item[0]))
        else:
            continue
        result.evaluation = item[1]
        result.save()
    
    print("done : save result")