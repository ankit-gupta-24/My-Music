from django.urls import path
from . import views

urlpatterns = [
    path('',views.index, name='index'),
    path('AddToFavourite/',views.AddToFavourite, name = 'AddToFavourites'),
    path('AddToLiked/',views.AddToLiked, name='AddToLiked'),
    path('CreatePlaylist/',views.CreatePlaylist, name='CreatePlaylist'),
    path('deletePlaylist/<int:pk>/',views.deletePlaylist,name='deletePlaylist'),
    path('getUserPlaylist/',views.getUserPlaylist, name='getUserPlaylist'),
    path('PlayPlaylist/',views.PlayPlaylist,name='PlayPlaylist'),
    path('AddSongToPlaylist/',views.AddSongToPlaylist, name='AddSongToPlaylist'),
    path('removeSongFromPlaylist/',views.removeSongFromPlaylist,name='removeSongFromPlaylist'),
    path('displayUserPlaylist/',views.displayUserPlaylist,name='displayUserPlaylist'),
    path('displaySinglePlaylist/<int:pk>/',views.displaySinglePlaylist,name='displaySinglePlaylist'),
    path('getUserFavouriteSongList/',views.getUserFavouriteSongList, name='getUserFavouriteSongList'),
    path('RemoveFromFavourite/',views.RemoveFromFavourite, name= 'RemoveFromFavourite'),
    path('getUserLikedSong/',views.getUserLikedSong, name='getUserLikedSong'),
    path('RemoveFromLiked/',views.RemoveFromLiked, name='RemoveFromLiked'),
    path('CategoryWiseSong/<str:category>/', views.CategoryWiseSong, name='CategoryWiseSong'),
    path('LanguageWiseSong/<str:language>/', views.LanguageWiseSong, name='LanguageWiseSong'),
    path('MovieWiseSong/<str:movieName>/',views.MovieWiseSong, name='MovieWiseSong'),
    path('ArtistWiseSong/<str:artist>/',views.ArtistWiseSong, name='ArtistWiseSong'),
    # path('StarWiseSong/<str:starName>/',views.StarWiseSong, name='StarWiseSong'),
    path('search/',views.search,name='search'),
    path('getSongSrc/',views.getSongSrc,name='getSongSrc'),
    path('shuffleAllSongs/',views.shuffleAllSongs,name='shuffleAllSongs'),
    path('allMovieTag',views.allMovieTag,name='allMovieTag'),
    path('allArtistTag',views.allArtistTag,name='allArtistTag'),
    path('sharedSong/<int:pk>/',views.sharedSong,name='sharedSong'),
]