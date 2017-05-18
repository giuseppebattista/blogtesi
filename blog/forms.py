from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Post


class SignUpFormUser(UserCreationForm):
    first_name = forms.CharField(max_length=30, help_text='nome')
    last_name = forms.CharField(max_length=30, help_text='cognome')
    email = forms.CharField(widget=forms.EmailInput)
    username = forms.CharField(max_length=30, help_text='username')
    matricola = forms.IntegerField(help_text='matricola')
    data_nascita = forms.DateField ( help_text='data di nascita')
    descrizione = forms.CharField(widget=forms.Textarea)

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'username', 'password1', 'password2', 'matricola',
                  'data_nascita','descrizione',)


class AddPost(forms.Form):
    descrizione = forms.CharField (widget=forms.Textarea,required=False, help_text='descrizione' )
    contenuto = forms.CharField (widget=forms.Textarea,required=False, help_text='contenuto' )
    slug = forms.SlugField(required=False)
    immagine = forms.ImageField(required=False,)
    title = forms.CharField (required=False,help_text='username' )
    class Meta:
        model= Post
