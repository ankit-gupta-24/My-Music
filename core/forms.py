from django.forms import ModelForm
from .models import Playlist
from django import forms

class PlaylistForm(ModelForm):
    class Meta:
        model = Playlist
        fields = '__all__'
        widgets = {
            'title':forms.TextInput(
                {
                    'class':'form-control mb-2',
                }),
            'playlist_logo':forms.FileInput(
                {
                    'class': 'form-control mb-2',
                }),
        }
