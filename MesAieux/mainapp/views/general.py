from django.shortcuts import render
from django.contrib import messages

from mainapp.forms import RechercheForm
from mainapp.models import Individu


def accueil(request):
    return render(request, 'mainapp/accueil.html', locals())


def mentionslegales(request):
    return render(request, 'mainapp/mentionslegales.html', locals())


def contact(request):
    return render(request, 'mainapp/contact.html', locals())


def recherche(request):
    if request.method == "POST":
        form = RechercheForm(request.POST)
        if form.is_valid():
            prenom = form.data['prenom']
            nom = form.data['nom']
            nationalite = form.data['nationalite']
            naissance = form.data['naissance']
            mariage = form.data['mariage']
            deces = form.data['deces']
            if prenom or nom or naissance or mariage or deces or nationalite:
                rechercher1 = Individu.objects
                if prenom:
                    rechercher1 = rechercher1.filter(user__first_name__iexact=prenom)
                if nom:
                    rechercher1 = rechercher1.filter(user__last_name__iexact=nom)
                if naissance:
                    rechercher1 = rechercher1.filter(date_nais=naissance)
                if mariage:
                    rechercher1 = rechercher1.filter(date_mariage=mariage)
                if deces:
                    rechercher1 = rechercher1.filter(date_dece=deces)
                if nationalite:
                    rechercher1 = rechercher1.filter(nationalite=nationalite.split('>')[2])
                return render(request, 'mainapp/recherche.html', {"rechercher": rechercher1})
            else:
                messages.add_message(request, messages.ERROR, "Aucun champs n'a été saisi")
        else:
            messages.add_message(request, messages.ERROR, "Les données saisies ne correspondent pas au format requis")
    return render(request, 'mainapp/recherche.html')
