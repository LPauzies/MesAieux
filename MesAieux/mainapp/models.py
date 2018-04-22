from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from datetime import datetime


class Famille(models.Model):
    nom = models.CharField(max_length=30)
    photo = models.ImageField(upload_to='famille/', default='famille/default.png')

    def __str__(self):
        return self.nom


class Coordonnee(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, default=1)
    numero = models.CharField(max_length=10, blank=True)
    nomrue = models.CharField(max_length=100, blank=True)
    ville = models.CharField(max_length=50, blank=True)
    code = models.CharField(max_length=5, blank=True)
    telephone = models.CharField(max_length=10, blank=True)

    class Meta:
        permissions = (
            ("hidden_address", "Peut cacher son adresse aux exterieurs a la famille"),
            ("hidden_telephone", "Peut cacher son telephone aux exterieurs a la famille"),
        )

    def __str__(self):
        return str(self.user)


User._meta.get_field('email')._unique = True


class Individu(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, default=1)
    famille = models.ForeignKey(Famille, blank=True, null=True)
    prenom2 = models.CharField(max_length=30, blank=True)
    prenom3 = models.CharField(max_length=30, blank=True)
    genre = models.CharField(max_length=30)
    date_nais = models.CharField(max_length=10)
    date_dece = models.CharField(max_length=10, blank=True, null=True)
    date_mariage = models.CharField(max_length=10, blank=True, null=True)
    nationalite = models.CharField(max_length=50)
    occupation = models.CharField(max_length=100, blank=True)
    photo = models.ImageField(upload_to='profil/', default='profil/default.png')

    def __str__(self):
        return str(self.user)

    class Meta:
        permissions = (
            ("admin_famille", "Peut administrer une famille"),
            ("confirmation", "Peut confirmer l'acces a une famille"),
            ("historien", "Peut valider ou non un document"),
        )


class Nom_Lien_Parente(models.Model):
    nom = models.CharField(max_length=30)

    def __str__(self):
        return self.nom


class Lien_Parente(models.Model):
    nom_lien_parente = models.ForeignKey(Nom_Lien_Parente)
    famille = models.ForeignKey(Famille)
    individu1 = models.ForeignKey(Individu, related_name='individu1', null=False)
    individu2 = models.ForeignKey(Individu, related_name='individu2', null=False)

    def __str__(self):
        return str(self.nom_lien_parente)


class Banque(models.Model):
    individu = models.ForeignKey(Individu)
    fichier = models.FileField(upload_to='uploads/')
    commentaire = models.TextField(max_length=500)
    tag = models.CharField(max_length=50, blank=True)
    validation = models.BooleanField(default=False)
    comHistorien = models.TextField(max_length=500, blank=True)
    dateHistorien = models.CharField(max_length=10, blank=True)

    def __str__(self):
        return str(self.individu)

    def split_tag(self):
        return self.tag.split(' ')


class Message(models.Model):
    user1 = models.ForeignKey(Individu, related_name='user1', null=False)
    user2 = models.ForeignKey(Individu, related_name='user2', null=False)
    message = models.TextField(max_length=300)
    date = models.DateTimeField(default=datetime.now, blank=True)

    def __str__(self):
        return str(self.message)
