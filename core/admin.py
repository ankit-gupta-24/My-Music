from django.contrib import admin
from .models import *
from django import forms
# Register your models here.

# I have customized django admin panel here


class SongAdminForm(forms.ModelForm):
    class Meta:
        model = Song
        fields = '__all__'

        widgets = {
            'songtime_in_seconds':forms.TextInput(
                attrs={
                    'placeholder':'e.g. 250',
                }
            ),
        }


@admin.register(Song)
class SongAdmin(admin.ModelAdmin):
    list_filter = ('publish_date','language')
    search_fields = ('title__contains',)
    form = SongAdminForm


@admin.register(Playlist)
class PlaylistAdmin(admin.ModelAdmin):
    pass

@admin.register(SongLike)
class SongLikeAdmin(admin.ModelAdmin):
    pass

@admin.register(SongFavourite)
class SongFavouriteAdmin(admin.ModelAdmin):
    pass