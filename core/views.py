from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import *
from .forms import *
from .utilityFunctions import *
from django.contrib import messages
from django.http import HttpResponse,JsonResponse
import json
from django.core import serializers
from django.core.serializers.json import DjangoJSONEncoder
import random
# Create your views here.

frm = PlaylistForm

def index(request):
    context = {}
    
    popular_songs = getPopularSongs()
    popular_90s = getPopular90s()
    recent_releases = getRecentReleases()
    all_languages = getLanguages()
    all_categories = getCategories()
    random_images = getRandomImage()

    context = {
        'popular_90s':popular_90s,
        'popular_songs': popular_songs,
        'recent_releases': recent_releases,
        'all_languages':all_languages,
        'all_categories':all_categories,
        'random_images':random_images,
        'frm':frm,
    }

    return render(request,'core/index.html',context)

@login_required(login_url='/accounts/loginForm/')
def AddToFavourite(request):
    if request.method == 'POST' and request.user.is_authenticated and request.is_ajax():
        song = Song.objects.get(id = int(request.POST.get('song_id')))
        added_by = User.objects.get(username=request.user.username)
        if SongFavourite.objects.filter(song=song,added_by=added_by).count() == 0 :
            fav_obj = SongFavourite(song=song,added_by=added_by)
            fav_obj.save()
            data = {
                'tag':'success',
                'msg':'Added to Favourite Songs',
            }
            return JsonResponse(data)
        data = {
                'tag':'info',
                'msg':'Already Added to Favourite Songs',
            }
        return JsonResponse(data)
    return HttpResponse('error')

@login_required(login_url='/accounts/loginForm/')
def RemoveFromFavourite(request):
    if request.method == 'POST' and request.user.is_authenticated and request.is_ajax():
        song = Song.objects.get(id = int(request.POST.get('song_id')))
        obj = SongFavourite.objects.get(song=song,added_by=request.user)
        obj.delete()
        return HttpResponse('success')
    return HttpResponse('error')

@login_required(login_url='/accounts/loginForm/')
def getUserFavouriteSongList(request):
    if request.user.is_authenticated:
        userFavSongs = SongFavourite.objects.filter(added_by=request.user)
        return render(request,'core/userFavList.html',{'favSongs':userFavSongs,'frm':frm,})
    return HttpResponse('error')

@login_required(login_url='/accounts/loginForm/')
def AddToLiked(request):
    if request.method == 'POST' and request.user.is_authenticated and request.is_ajax():
        sid = int(request.POST.get('song_id'))
        song = Song.objects.get(id = sid )
        liked_by = User.objects.get(username=request.user.username)
        if SongLike.objects.filter(song=song,liked_by=liked_by).count() == 0:
            like_obj = SongLike(song=song,liked_by=liked_by)
            like_obj.save()
            data = {
                'tag':'success',
                'msg':'Added to Liked Songs',
            }
            return JsonResponse(data)
        data = {
                'tag':'info',
                'msg':'Already Added to Liked Songs',
            }
        return JsonResponse(data)
    return HttpResponse('error')

@login_required(login_url='/accounts/loginForm/')
def RemoveFromLiked(request):
    if request.method == 'POST' and request.user.is_authenticated and request.is_ajax():
        song = Song.objects.get(id = int(request.POST.get('song_id')))
        obj = SongLike.objects.get(song=song,liked_by=request.user)
        obj.delete()
        return HttpResponse('success')
    return HttpResponse('error')

@login_required(login_url='/accounts/loginForm/')
def getUserLikedSong(request):
    if request.user.is_authenticated:
        userLikedSong = SongLike.objects.filter(liked_by=request.user)
        return render(request,'core/userLikedSongList.html',{'LikedSong':userLikedSong,'frm':frm,})
    return HttpResponse('error')

def CategoryWiseSong(request,category):
    category_songs = []
    for elem in CategoryChoices:
        if category in elem[1]:
            category_songs= Song.objects.filter(category=elem[0])
            break
    
    context = {
        'category':category,
        'category_songs': category_songs,
        'frm':frm,
    }
    return render(request,'core/TagWiseSong.html', context)

def LanguageWiseSong(request,language):
    language_songs = []
    for lang in LanguageChoices:
        if language in lang[1]:
            language_songs = Song.objects.filter(language=lang[0])
            break

    context = {
        'category':language,
        'category_songs':language_songs,
        'frm':frm,
    }
    return render(request,'core/TagWiseSong.html',context)

def MovieWiseSong(request,movieName):
    movie_songs = Song.objects.filter(movie_name__contains=movieName)
    context = {
        'category':movieName,
        'category_songs':movie_songs,
        'frm':frm,
    }
    return render(request,'core/TagWiseSong.html',context)

def ArtistWiseSong(request,artist):
    artist_songs = Song.objects.filter(singer__contains = artist)

    context = {
        'category':artist,
        'category_songs':artist_songs,
        'frm':frm,
    }
    return render(request,'core/TagWiseSong.html',context)

# def StarWiseSong(request,starName):
#     star_songs = Song.objects.filter(actor_actress__contains=starName)
#     context = {
#         'category':starName,
#         'category_songs':star_songs
#     }
#     return render(request,'core/TagWiseSong.html',context)

def search(request):
    searched_songs =set()
    searchKey = request.POST.get('searchkey').lower()
    print(searchKey)
    for song in Song.objects.all():
        if (song.singer and searchKey in song.singer.lower()) or (song.movie_name and searchKey in song.movie_name.lower()) or (song.actor_actress and searchKey in song.actor_actress.lower()) or (song.title and searchKey in song.title.lower()):
            searched_songs.add(song)

    for lang in LanguageChoices:
        if searchKey in lang[1].lower():
            searched_songs.update(Song.objects.filter(language=lang[0]))
            break
    for elem in CategoryChoices:
        if searchKey in elem[1].lower():
            searched_songs.update(Song.objects.filter(category=elem[0]))
            break

    context ={
        'category':searchKey,
        'category_songs':searched_songs,
        'frm':frm,
    }
    return render(request,'core/TagWiseSong.html',context)

def getSongSrc(request):
    if request.method == 'POST' and request.is_ajax():
        song = None
        if int(request.POST.get('song_id')) > Song.objects.all().count():
            song = Song.objects.filter(id=1).values('id','title','audio_file','song_image','songtime_in_seconds')            
        elif int(request.POST.get('song_id')) < 1:
            song = Song.objects.filter(id=Song.objects.all().count()//2).values('id','title','audio_file','song_image','songtime_in_seconds')            
        else:
            song = Song.objects.filter(id=int(request.POST.get('song_id'))).values('id','title','audio_file','song_image','songtime_in_seconds')
       
        song = json.dumps(list(reversed(song)), cls=DjangoJSONEncoder)
        data = {
            'obj':song,
        }
        return JsonResponse(data)
    return HttpResponse('error')

def shuffleAllSongs(request):
    if request.method == 'POST' and request.is_ajax():
        id = random.randint(1,Song.objects.all().count())
        song = Song.objects.filter(id=id).values('id','title','audio_file','song_image','songtime_in_seconds')
        song = json.dumps(list(reversed(song)), cls=DjangoJSONEncoder)
        data = {
            'obj':song,
        }
        return JsonResponse(data)
    return HttpResponse('error')

def allArtistTag(request):
    context = {
        'tags':getPopularArtist(),
        'art':True,
        'frm':frm,
    }
    return render(request,'core/displayAllTags.html',context)

def allMovieTag(request):
    context = {
        'tags':getMoviesName(),
        'art':False,
        'frm':frm,
    }
    return render(request,'core/displayAllTags.html',context)


@login_required(login_url='/accounts/loginForm/')
def CreatePlaylist(request):
    if request.method == 'POST' and request.user.is_authenticated:
        p_title = request.POST.get('title')
        p_user = request.user
        p_img = request.FILES.get('playlist_logo')
        frm = Playlist(title=p_title ,user=p_user , playlist_logo=p_img )

        frm.save()
        return redirect('displayUserPlaylist')
    else:
        return HttpResponse('error')

@login_required(login_url='/accounts/loginForm/')
def displayUserPlaylist(request):
    all_user_playlist = Playlist.objects.filter(user=request.user)
    return render(request,'core/displayPlaylists.html',{'all_user_playlist':all_user_playlist,'frm':frm,})
    # return HttpResponse('all playlist of user')

@login_required(login_url='/accounts/loginForm/')
def displaySinglePlaylist(request,pk):
    playlist = Playlist.objects.get(id=int(pk))
    context = {
        'title':playlist.title,
        'src':playlist.playlist_logo,
        'id':playlist.id,
        'playlist_songs':playlist.songs.all(),
        'songCount':playlist.songs.count(),
        'frm':frm,
    }
    # print(playlist.songs)
    return render(request,'core/displaySinglePlaylist.html',context)

@login_required(login_url='/accounts/loginForm/')
def getUserPlaylist(request):
    playlist = Playlist.objects.filter(user=request.user).values('id','title')
    playlist = json.dumps(list(reversed(playlist)), cls=DjangoJSONEncoder)
    data = {
        'playlist':playlist,
    }
    return JsonResponse(data)

@login_required(login_url='/accounts/loginForm/')
def AddSongToPlaylist(request):
    if request.method == 'POST':
        sid = int(request.POST.get('sid'))
        pid = int(request.POST.get('pid'))

        song = Song.objects.get(id=sid)
        pl = Playlist.objects.get(id=pid)
        pl.songs.add(song)
        data = {
            'tag':'success',
            'msg':'Added to Playlist',
        }
        return JsonResponse(data)
    data = {
        'tag':'danger',
        'msg':'Failed to add Playlist',
    }
    return JsonResponse(data)

@login_required(login_url='/accounts/loginForm/')
def removeSongFromPlaylist(request):
    if request.method == 'POST':
        sid = int(request.POST.get('sid'))
        pid = int(request.POST.get('pid'))

        song = Song.objects.get(id=sid)
        pl = Playlist.objects.get(id=pid)
        pl.songs.remove(song)
        return HttpResponse('success')
    return HttpResponse('error')

@login_required(login_url='/accounts/loginForm/')
def deletePlaylist(request,pk):
    if request.user.is_authenticated:
        pl = Playlist.objects.get(id=pk)
        pl.delete()
    return redirect('displayUserPlaylist')

@login_required(login_url='/accounts/loginForm/')
def PlayPlaylist(request):
    if request.method == 'POST':
        pk = request.POST.get('pid')
        playlist = Playlist.objects.get(id=int(pk))
        context = {
            'playlist_songs':json.dumps(list(reversed(playlist.songs.all().values('id','title'))),cls=DjangoJSONEncoder),
            'songCount':playlist.songs.count(),
        }
        return JsonResponse(context)
    else:
        return HttpResponse('error')

def sharedSong(request,pk):
    song = Song.objects.filter(id=pk)
    context ={
        'category':'Shared',
        'category_songs': song,
        'frm':frm,
    }
    return render(request,'core/TagWiseSong.html',context)