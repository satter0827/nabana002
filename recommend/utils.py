import requests
import random
import shutil
import bs4
import ssl
import pandas as pd
from collections import defaultdict
from surprise import SVD, SVDpp,KNNBasic
from surprise import Reader, Dataset

from django_pandas.io import read_frame
from recommend.models import Anime, Rating, Result, ResultKNN

ssl._create_default_https_context = ssl._create_unverified_context

def download_img(data):
  Res = requests.get("https://www.google.com/search?hl=jp&q=" + data + "&btnG=Google+Search&tbs=0&safe=off&tbm=isch")
  Html = Res.text
  Soup = bs4.BeautifulSoup(Html,'lxml')
  links = Soup.find_all("img", limit=2)
  #link = random.choice(links).get("src")

  if len(links) > 1:
    link = links[1].get("src")
    r = requests.get(link, stream=True)

    if r.status_code == 200:
      return r.url
    else:
      return ""
  else:
    return ""

def register_result(rec_algo):
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

  if rec_algo == "SVD":
    algo = SVD()
  else:
    algo = KNNBasic(k=5, min_k=1,sim_options=sim_options)
  algo.fit(trainset)

  # そして学習用データに含まれていない全ての（ユーザ、アイテムの）組み合わせに対して評価を予測する。
  testset = trainset.build_anti_testset()
  predictions = algo.test(testset)

  top_n = get_top_n(predictions, n=10)

  if rec_algo == "SVD":
    Result.objects.all().delete()
  else:
    ResultKNN.objects.all().delete()

  for key in top_n:
    unit = top_n[key]
    for item in unit:
      if rec_algo == "SVD":
        result = Result()
      else:
        result = ResultKNN()
      result.user_id = key
      if len(key) != 36:
        continue
      if Anime.objects.filter(anime_id=int(item[0])):
        result.anime_id = Anime.objects.get(anime_id=int(item[0]))
      else:
        continue
      result.evaluation = item[1]
      result.save()

  print("update_reccommend")

def get_top_n(predictions, n=10):
  top_n = defaultdict(list)
  for uid, iid, _, est, _ in predictions:
    top_n[uid].append((iid, est))

  # そして各ユーザに対して予測値をソートして最も高いk個を返す。
  for uid, user_ratings in top_n.items():
    user_ratings.sort(key=lambda x: x[1], reverse=True)
    top_n[uid] = user_ratings[:n]

  return top_n