import requests
import random
import shutil
import bs4
import ssl

from django_pandas.io import read_frame
from recommend.models import Anime, Rating

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
