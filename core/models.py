from django.db import models
from django.contrib.auth.models import User
# from django.core.files.storage import FileSystemStorage
# from django.conf import settings
# import os

# Create your models here.

# fs = FileSystemStorage(location=os.path.join(settings.BASE_DIR,'/media/'))



CategoryChoices = [
        ('BR','Bollywood Romantic'),
        ('HR','Hollywood Romantic'),
        ('BRA','Bollywood Romantic Action'),
        ('BR','Bollywood Rock'),
        ('BNR','Bollywood Nineties 90s Romantic'),
        ('BER','Bollywood Eighties 80s Romantic'),
        ('BRUP','BreakUp Song'),
        ('BF','Best Friend'),
        ('FLR','First Love Romantic'),
        ('FS','Family Songs'),
        ('CH','Childhood Bachapan'),
        ('AGB','Anger Battle'),
        ('DD','Dancing DJ Rock'),
        ('LRH','Love Romantic Heart'),
        ('BW','Bollywood'),
        ('HW','HollyWood'),
        ('VN','Valentine Love'),
        ('RG','Religious'),
        ('AR','Arties Bhajan'),
        ('DB','Patriotism Desh Bhakti DeshBhakti'),
        ('RAL','Revenge Anger Love'),
        ('RM','Romantic'),
        ('LV','Love'),
    ]

LanguageChoices = [
    ('HN','Hindi'),
    ('EN','English'),
    ('PB','Punjabi'),
    ('TM','Tamil'),
    ('TL','Telugu'),
    ('MH','Marathi'),
    ('GJ','Gujrati'),
    ('BJ','Bhoojpuri'),
    ('HR','Haryanvi'),
    ('RJ','Rajasthani'),
]

# model to store songs; only superuser or staff user can add songs
class Song(models.Model):
    title = models.CharField(max_length=100) #song name
    audio_file= models.FileField(upload_to='audioFiles/')
    song_image = models.FileField(upload_to='images/' ,null=True, blank=True)
    songtime_in_seconds = models.CharField(max_length=4)
    publish_date = models.DateField(null=True,blank=True)
    singer = models.CharField(max_length=100) #singer name
    actor_actress = models.CharField(max_length=300)
    movie_name = models.CharField(max_length=100,blank=True,null=True)
    category = models.CharField(max_length=5,choices=CategoryChoices)
    language = models.CharField(max_length=2,choices=LanguageChoices)

    class Meta:
        ordering = ('title','publish_date',)

    def __str__(self):
        return self.title

# model to store playlist created by user
class Playlist(models.Model):
    title = models.CharField(max_length=100)
    songs = models.ManyToManyField(Song,null=True,blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    playlist_logo = models.FileField(upload_to = 'images/playlist_logo/')

    def __str__(self):
        return self.title

# model to store like when user likes song
class SongLike(models.Model):
    song = models.ForeignKey(Song , on_delete=models.CASCADE)
    liked_by = models.ForeignKey(User, on_delete=models.CASCADE)

# model to store favourite song of user
class SongFavourite(models.Model):
    song = models.ForeignKey(Song, on_delete=models.CASCADE)
    added_by = models.ForeignKey(User, on_delete=models.CASCADE)