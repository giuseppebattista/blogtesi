from django.db import models
from django.utils import timezone
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.contrib.auth.models import User

# Create your models here.
class Studente(models.Model):
    matricola = models.IntegerField(unique=True)
    descrizione = models.TextField(max_length=500, blank=True)
    data_nascita = models.DateField(blank=True , null=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    @receiver ( post_save, sender=User )
    def ensure_student_exists(sender, **kwargs):
        if kwargs.get ( 'created', False ):
            Studente.objects.get_or_create ( user=kwargs.get ( 'instance' ) )


class MaterialeDidattico(models.Model):
    id_materiale = models.AutoField(primary_key=True)
    nome = models.CharField(max_length=50, null=False)
    file = models.FileField(upload_to='materiale_didattico/')
    materia = models.CharField(max_length=500)
    matricola = models.ForeignKey(Studente)
    data_caricamento = models.DateTimeField(default=timezone.now)

    def __unicode__(self):
        return self.nome


class Categoria(models.Model):
    id_categoria = models.AutoField(primary_key=True)
    nome = models.CharField(max_length=50, null=False)

    def __unicode__(self):
        return self.nome


class Admin(models.Model):
    id_admin = models.AutoField(primary_key=True)
    nome = models.CharField(max_length=30, null=False)
    cognome = models.CharField(max_length=30)
    username = models.CharField(max_length=16, null=False, unique=True)
    password = models.CharField(max_length=16, unique=True, null=False)
    email = models.EmailField(unique=True, null=False)

    def __unicode__(self):
        return self.username


class Post(models.Model):
    id_post = models.AutoField(primary_key=True)
    title = models.CharField(max_length=200, null=False, unique=True)
    descrizione = models.TextField(max_length=500)
    contenuto = models.TextField()
    immagine = models.ImageField(upload_to='post/images/')
    slug = models.SlugField(unique=True)
    autore = models.ForeignKey(Studente)
    data_creazione = models.DateTimeField(default=timezone.now)
    id_admin = models.ForeignKey(Admin, null=True)
    data_pubblicazione = models.DateTimeField(blank=True, null=True)

    def crea(self):
        self.data_creazione= timezone.now()
        self.save()

    def pubblica(self):
        self.data_pubblicazione = timezone.now()
        self.save()

    def __unicode__(self):
        return self.title


class Tag(models.Model):
    id_tag = models.AutoField(primary_key=True)
    nome = models.CharField(max_length=30, null=False)
    slug = models.SlugField(unique=True)

    def __unicode__(self):
        return self.nome


class Scarica(models.Model):
    matricola = models.ForeignKey(Studente)
    id_materiale = models.ForeignKey(MaterialeDidattico)
    data_download = models.DateTimeField(default=timezone.now)


class AppartieneA(models.Model):
    id_post = models.ForeignKey(Post)
    id_categoria = models.ForeignKey(Categoria)


class HaAssociato(models.Model):
    id_post = models.ForeignKey(Post)
    id_tag = models.ForeignKey(Tag)