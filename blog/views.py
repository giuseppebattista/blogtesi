from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from .forms import SignUpFormUser
from .forms import AddPost
from django.db import transaction
from django.contrib.auth.models import Group
from .models import Studente
from .models import Post


@transaction.atomic
def signup(request):
    if request.method == 'POST':
        user_form = SignUpFormUser ( request.POST )
        if user_form.is_valid ():
            user = user_form.save ()
            user.refresh_from_db ()  # load the profile instance created by the signal
            # user.studente.data_nascita = user_form.cleaned_data.get('data_nascita')
            # user.studente.matricola = user_form.cleaned_data.get('matricola')
            user.save ()
            user.groups.add ( Group.objects.get ( name='Studente' ) )
            studente = Studente.objects.get ( user_id=user.id )
            studente.matricola = user_form.cleaned_data.get ( 'matricola' )
            studente.data_nascita = user_form.cleaned_data.get ( 'data_nascita' )
            studente.descrizione = user_form.cleaned_data.get ( 'descrizione' )
            studente.save ()
    else:
        user_form = SignUpFormUser ()
    return render ( request, 'blog/signup.html', {'form': user_form} )

@login_required
def addPost(request):
    if request.method == 'POST':
        form = AddPost ( request.POST, request.FILES)
        if form.is_valid ():
            studente = Studente.objects.get ( pk=11 )
            post = Post()
            post.title = form.cleaned_data.get ( 'title' )
            post.descrizione = form.cleaned_data.get ( 'descrizione' )
            post.contenuto = form.cleaned_data.get ( 'contenuto' )
            post.immagine = form.cleaned_data.get ( 'immagine' )
            post.slug = form.cleaned_data.get ( 'slug' )
            post.autore=studente
            post.data_creazione=timezone.now()
            #studente = Studente.objects.get ( id=11 )
            #post.autore_id = studente
            post.save ()
    else:
        form = AddPost ()
    return render ( request, 'blog/addpost.html', {'form': form} )


def home(request):
    return render (request, 'blog/index.html')

def login(request):
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(username=username, password=password)
    if user is not None:
        login(request,user)
        return render (request,'blog/index.html')
