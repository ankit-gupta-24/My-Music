import datetime
from datetime import date
from collections import Counter
from .models import *
from pathlib import Path
import os
from random import choice

BASE_DIR = Path(__file__).resolve().parent.parent

def getRandomImage():
    dir_path = os.path.join(BASE_DIR, 'media/images/')
    files = [content for content in os.listdir(dir_path) if os.path.isfile(os.path.join(dir_path, content))]
    return files


def getPopularSongs():
    all_likes = SongLike.objects.all().values('song')
    all_liked_songs = []
    for elem in all_likes:
        all_liked_songs.append(Song.objects.get(id=elem['song']))
    # print(all_liked_songs)
    all_liked_songs_dict = list(dict(Counter(all_liked_songs)))[:10]
    # print(all_liked_songs_dict)
    return all_liked_songs_dict

def getPopular90s():
    d =datetime.date(2000,1,1)
    op= []
    count = 0
    for obj in Song.objects.all():
        if obj.publish_date < d:
            op.append(obj)
            count += 1
        if count>10:
            break
    return op

def getRecentReleases():
    d = date.today()
    d = datetime.date(d.year,d.month-1,d.day)
    op= []
    count = 0

    for obj in Song.objects.all():
        if obj.publish_date >= d:
            op.append(obj)
            count+=1
        if count>20:
            break
    op = list(sorted(op,key=lambda x: x.publish_date,reverse=True))
    return op

def getPopularArtist():
    all_artist = Song.objects.all().values('singer')
    op = []
    for elem in all_artist:
        op.extend(elem['singer'].split(','))
    return set(op)

def getPopularStar():
    all_star = Song.objects.all().values('actor_actress')
    op = []
    for elem in all_star:
        op.extend(elem['actor_actress'].split(','))
    op = [i for i in op if i]
    return set(op)

def getCategories():
    all_categories = []
    for elem in CategoryChoices:
        all_categories.append(elem[1])

    return list(set(all_categories))

def getLanguages():
    all_languages =[]
    for elem in LanguageChoices:
        all_languages.append(elem[1])
    return all_languages
    

def getMoviesName():
    all_movies_obj = Song.objects.all().values('movie_name')
    all_movies = set()
    for elem in all_movies_obj:
        if elem['movie_name']:
            all_movies.add(elem['movie_name'])
    # print(all_movies)
    return all_movies

