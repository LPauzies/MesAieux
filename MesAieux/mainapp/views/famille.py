import json
import copy

from django.shortcuts import render
from django.contrib.auth.models import User
# from django.db import IntegrityError
# from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseNotFound, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from django.urls import reverse
from django.contrib import messages
from django.db import IntegrityError
from django.core.exceptions import ObjectDoesNotExist
from django.utils.datastructures import MultiValueDictKeyError

from mainapp.models import Famille, Individu, Nom_Lien_Parente, Lien_Parente
from mainapp.forms import ImageUploadForm, MembreForm, AjoutLienParenteForm


@csrf_exempt
@login_required
def creerfamille(request):
    """
    File: famille.py
    Author: Antoine Bourgeois
    Email: bourgeoisa@eisti.eu
    Date: 2016-12-21
    Description: Fonction permettant la création d'une famille en la sauvegardant dans la bdd
    """
    if request.method == 'POST':
        post = request.POST['nom_famille']
        nomfamille = json.loads(post)
        famille = Famille(nom=nomfamille)
        famille.save()
        famille.individu_set.add(request.user.individu)
        content_type = ContentType.objects.get_for_model(Individu)
        permission = Permission.objects.get(content_type=content_type, codename='admin_famille')
        request.user.user_permissions.add(permission)
        request.user.save()
        json_data = json.dumps({"HTTPRESPONSE": nomfamille})
        return HttpResponse(json_data)
    else:
        return HttpResponseNotFound('<h1>Page not found</h1>')


@csrf_exempt
@login_required
def rejoindreFamille(request):
    """
    File: famille.py
    Author: Antoine Bourgeois
    Email: bourgeoisa@eisti.eu
    Date: 2016-12-21
    Description: Permet à l'utilisateur de demander à un admin de rejoindre une famille
    """
    if request.method == 'POST':
        try:
            post = request.POST['nom_famille_rejoindre']
            nomFamille = json.loads(post)
            nomRejoindreFamille = Famille.objects.get(nom=nomFamille)
            nomRejoindreFamille.individu_set.add(request.user.individu)
            content_type = ContentType.objects.get_for_model(Individu)
            permission = Permission.objects.get(content_type=content_type, codename='confirmation')
            request.user.user_permissions.add(permission)
            request.user.save()
            json_data = json.dumps({"HTTPRESPONSE": nomFamille})
            return HttpResponse(json_data)
        except:
            messages.add_message(request, messages.INFO, "La famille demandé n'existe pas.")
            return HttpResponseRedirect(reverse('accueil'))
    else:
        return HttpResponseNotFound('<h1>Page not found</h1')

# -------- Creation Arbre ------------


def triParent(lienParents):
    """
    File: famille.py
    Author: Antoine Bourgeois
    Email: bourgeoisa@eisti.eu
    Date: 2016-12-21
    Description: Trie une liste pour que les parents soit au début en fonction de leurs ages.
    """
    # Trie le tableau pour avoir les parents en premier
    i = 0
    acc = 0
    while (i != len(lienParents)):
        if (lienParents[i].nom_lien_parente.id == 2):
            change = lienParents[acc]
            lienParents[acc] = lienParents[i]
            lienParents[i] = change
            acc = acc + 1

        i = i + 1
    return lienParents


def cmp_to_key(mycmp):
    """
    File: famille.py
    Author: Antoine Bourgeois
    Email: bourgeoisa@eisti.eu
    Date: 2016-12-21
    Description: convertie une fontion compare(cmp) en fonction clef(key)
    """
    class K:
        def __init__(self, obj, *args):
            self.obj = obj

        def __lt__(self, other):
            return mycmp(self.obj, other.obj) < 0

        def __gt__(self, other):
            return mycmp(self.obj, other.obj) > 0

        def __eq__(self, other):
            return mycmp(self.obj, other.obj) == 0

        def __le__(self, other):
            return mycmp(self.obj, other.obj) <= 0

        def __ge__(self, other):
            return mycmp(self.obj, other.obj) >= 0

        def __ne__(self, other):
            return mycmp(self.obj, other.obj) != 0
    return K


def compAge(user1, user2):
    """
    File: famille.py
    Author: Antoine Bourgeois
    Email: bourgeoisa@eisti.eu
    Date: 2016-12-21
    Description: compare l'age de deux individu
    """
    if int(user1.individu2.date_nais[6:]) < int(user2.individu2.date_nais[6:]):
        return -1
    elif int(user1.individu2.date_nais[6:]) > int(user2.individu2.date_nais[6:]):
        return 1
    else:
        return 0


def compAgeListe(liste1, liste2):
    """
    File: famille.py
    Author: Antoine Bourgeois
    Email: bourgeoisa@eisti.eu
    Date: 2016-12-21
    Description: compare l'age de deux individu dans deux listes différentes
    """
    if int(liste1[0]["age"]) < int(liste2[0]["age"]):
        return -1
    elif int(liste1[0]["age"]) > int(liste2[0]["age"]):
        return 1
    else:
        return 0


def triListeAge(liste1):
    """
    File: famille.py
    Author: Antoine Bourgeois
    Email: bourgeoisa@eisti.eu
    Date: 2016-12-21
    Description: Trie une liste de manière croissante selon l'age des individus
    """
    return sorted(liste1, key=cmp_to_key(compAge))


def triListeListeAge(liste1):
    """
    File: famille.py
    Author: Antoine Bourgeois
    Email: bourgeoisa@eisti.eu
    Date: 2016-12-21
    Description: trie une liste de liste selon l'age de l'individu
    """
    return sorted(liste1, key=cmp_to_key(compAgeListe))


def creationArbre(liste, i, enfant, j):
    """
    File: famille.py
    Author: Antoine Bourgeois
    Email: bourgeoisa@eisti.eu
    Date: 2016-12-21
    Description: Créer l'arbre de la famille en Json à partir d'une liste de liste de dictionnaire.
    """
    if i >= len(liste[j]) - 1 and 'spouse' not in liste[j][i] and 'parent' not in liste[j][i]:
        if enfant == []:
            arbre = {
                "class": liste[j][i]["class"],
                "name": liste[j][i]["name"],
                "extra": {
                    "photo": liste[j][i]["photo"],
                    "genre": liste[j][i]["genre"],
                    "dateNais": liste[j][i]["dateNais"],
                    "dateDece": liste[j][i]["dateDece"]
                },
            }
            enfant.append(arbre)
            return enfant
        else:
            return enfant
    elif 'parent' not in liste[j][i] and 'mari' in liste[j][i]:
        arbre = {
            "name": liste[j][i]["name"],
            "class": liste[j][i]["class"],
            "extra": {
                "photo": liste[j][i]["photo"],
                "genre": liste[j][i]["genre"],
                "dateNais": liste[j][i]["dateNais"],
                "dateDece": liste[j][i]["dateDece"]
            },
            "marriages": [creationArbre(liste, i + 1, enfant, j)]
        }
        return arbre
    elif 'parent' in liste[j][i] and 'mari' not in liste[j][i] and 'firstChild' not in liste[j][i]:
        arbre = {
            "name": liste[j][i]["name"],
            "class": liste[j][i]["class"],
            "extra": {
                "photo": liste[j][i]["photo"],
                "genre": liste[j][i]["genre"],
                "dateNais": liste[j][i]["dateNais"],
                "dateDece": liste[j][i]["dateDece"]
            },
            "children": creationArbre(liste, i + 1, enfant, j)
        }
        return arbre
    elif ('enfant' in liste[j][i] or 'parent' in liste[j][i]) and 'mari' in liste[j][i]:
        arbre = {
            "name": liste[j][i]["name"],
            "class": liste[j][i]["class"],
            "extra": {
                "photo": liste[j][i]["photo"],
                "genre": liste[j][i]["genre"],
                "dateNais": liste[j][i]["dateNais"],
                "dateDece": liste[j][i]["dateDece"]
            },
            "marriages": creationArbre(liste, i + 1, enfant, j)
        }
        return arbre
    elif 'spouse' in liste[j][i] and i < len(liste[j]) - 1:
        arbre = {
            "spouse": {
                "class": liste[j][i]["class"],
                "name": liste[j][i]["name"],
                "extra": {
                    "photo": liste[j][i]["photo"],
                    "genre": liste[j][i]["genre"],
                    "dateNais": liste[j][i]["dateNais"],
                    "dateDece": liste[j][i]["dateDece"]
                },
            },
            "children": creationArbre(liste, i + 1, enfant, j)
        },
        return arbre
    elif 'spouse' in liste[j][i]:
        arbre = {
            "spouse": {
                "class": liste[j][i]["class"],
                "name": liste[j][i]["name"],
                "extra": {
                    "photo": liste[j][i]["photo"],
                    "genre": liste[j][i]["genre"],
                    "dateNais": liste[j][i]["dateNais"],
                    "dateDece": liste[j][i]["dateDece"]
                },
            }
        }
        return arbre
    elif 'enfant' in liste[j][i] and 'mari' not in liste[j][i]:
        newEnfant = []
        acc = j
        while i <= len(liste[acc]) - 1:
            if 'parent' in liste[acc][i] and j <= len(liste):
                j = j + 1
                newEnfant.append(creationArbre(liste, 0, [], j))
            else:
                arbre = {
                    "class": liste[acc][i]["class"],
                    "name": liste[acc][i]["name"],
                    "extra": {
                        "photo": liste[acc][i]["photo"],
                        "genre": liste[acc][i]["genre"],
                        "dateNais": liste[acc][i]["dateNais"],
                        "dateDece": liste[acc][i]["dateDece"]
                    },
                }
                newEnfant.append(arbre)
            i = i + 1
        return newEnfant
    else:
        return {
            "class": liste[j][i]["class"],
            "name": liste[j][i]["name"],
            "extra": {
                "photo": liste[j][i]["photo"],
                "genre": liste[j][i]["genre"],
                "dateNais": liste[j][i]["dateNais"],
                "dateDece": liste[j][i]["dateDece"]
            },
        }


def creationListe(lienParents):
    """
    File: famille.py
    Author: Antoine Bourgeois
    Email: bourgeoisa@eisti.eu
    Date: 2016-12-21
    Description: Créer une liste de liste de dictionnaire pour créer l'arbre
    """
    newArbre = []
    bigArbre = []
    name1 = ""
    name2 = ""
    longListe = len(lienParents)
    i = 0
    while i <= longListe - 1:
        ajoutArbre = {}
        if name1 == lienParents[i].individu1.user.first_name + ' ' + lienParents[i].individu1.user.last_name or name2 == lienParents[i].individu1.user.first_name + ' ' + lienParents[i].individu1.user.last_name:
            ajoutArbre["name"] = lienParents[i].individu2.user.first_name + ' ' + lienParents[i].individu2.user.last_name
            ajoutArbre["photo"] = lienParents[i].individu2.photo.name
            ajoutArbre["genre"] = lienParents[i].individu2.genre
            ajoutArbre["dateNais"] = lienParents[i].individu2.date_nais
            if lienParents[i].individu2.date_dece:
                ajoutArbre["dateDece"] = lienParents[i].individu2.date_dece
            else:
                ajoutArbre["dateDece"] = ''
            ajoutArbre["age"] = lienParents[i].individu2.date_nais[6:]
            if lienParents[i].individu2.genre == "femme":
                ajoutArbre["class"] = "woman"
            else:
                ajoutArbre["class"] = "man"
            ajoutArbre["enfant"] = ""
            newArbre.append(ajoutArbre)
            if i == longListe - 1:
                bigArbre.append(newArbre)
        else:
            if i != 0:
                bigArbre.append(newArbre)
                newArbre = []
            ajoutArbre["name"] = lienParents[i].individu1.user.first_name + ' ' + lienParents[i].individu1.user.last_name
            ajoutArbre["age"] = lienParents[i].individu1.date_nais[6:]
            ajoutArbre["photo"] = lienParents[i].individu1.photo.name
            ajoutArbre["genre"] = lienParents[i].individu1.genre
            ajoutArbre["dateNais"] = lienParents[i].individu1.date_nais
            if lienParents[i].individu1.date_dece:
                ajoutArbre["dateDece"] = lienParents[i].individu1.date_dece
            else:
                ajoutArbre["dateDece"] = ''
            if lienParents[i].individu1.genre == "femme":
                ajoutArbre["class"] = "woman"
            else:
                ajoutArbre["class"] = "man"
            if i == 0:
                ajoutArbre["parent"] = ""
            name1 = lienParents[i].individu1.user.first_name + ' ' + lienParents[i].individu1.user.last_name
            name2 = lienParents[i].individu2.user.first_name + ' ' + lienParents[i].individu2.user.last_name
            if lienParents[i].nom_lien_parente.id == 2:
                ajoutArbre["mari"] = ""

            if i == longListe - 1:
                newArbre = []
                newArbre.append(ajoutArbre)
            else:
                newArbre.append(ajoutArbre)
            ajoutArbre = {}
            ajoutArbre["name"] = lienParents[i].individu2.user.first_name + ' ' + lienParents[i].individu2.user.last_name
            ajoutArbre["age"] = lienParents[i].individu2.date_nais[6:]
            ajoutArbre["photo"] = lienParents[i].individu2.photo.name
            ajoutArbre["genre"] = lienParents[i].individu2.genre
            ajoutArbre["dateNais"] = lienParents[i].individu2.date_nais
            if lienParents[i].individu2.date_dece:
                ajoutArbre["dateDece"] = lienParents[i].individu2.date_dece
            else:
                ajoutArbre["dateDece"] = ''
            if lienParents[i].individu2.genre == "femme":
                ajoutArbre["class"] = "woman"
            else:
                ajoutArbre["class"] = "man"
            if lienParents[i].nom_lien_parente.id == 2:
                ajoutArbre["spouse"] = ""
            else:
                ajoutArbre["enfant"] = ""
            if i == longListe - 1:
                newArbre.append(ajoutArbre)
                bigArbre.append(newArbre)
            else:
                newArbre.append(ajoutArbre)
        i = i + 1
    return bigArbre


def rechercheParent(liste):
    """
    File: famille.py
    Author: Antoine Bourgeois
    Email: bourgeoisa@eisti.eu
    Date: 2016-12-21
    Description: Recherche les parents de la famille pour leurs mettre l'attribut parent.
    """
    i = 0
    j = 0
    acc = 0
    while i < len(liste) - 1 and acc < len(liste) - 1:
        while j <= len(liste[i]) - 1 and acc < len(liste) - 1:
            if liste[i][j]["name"] == liste[acc + 1][0]["name"] and 'parent' not in liste[i][j]:
                liste[i][j]["parent"] = ""
                if len(liste[acc + 1]) > 2:
                    liste[acc + 1][0]["parent"] = ""
                elif len(liste[acc + 1]) == 2 and 'enfant' in liste[acc + 1][1]:
                    liste[acc + 1][0]["parent"] = ""
                acc = acc + 1
            j = j + 1
        j = 0
        i = i + 1
    return liste


def makeFirstChild(liste):
    """
    File: famille.py
    Author: Antoine Bourgeois
    Email: bourgeoisa@eisti.eu
    Date: 2016-12-21
    Description: Recherche les premier enfants de chaque couple.
    """
    i = 0
    j = 0
    while i < (len(liste) - 1):
        while j <= len(liste[i]) - 1 and i < (len(liste) - 1):
            if "parent" not in liste[i][j] and "spouse" not in liste[i][j]:
                liste[i][j]["firstChild"] = ""
                i = i + 1
                j = 0
            j = j + 1
        j = 0
        i = i + 1
    return liste


@csrf_exempt
def famille(request):
    """
    File: famille.py
    Author: Antoine Bourgeois
    Email: bourgeoisa@eisti.eu
    Date: 2016-12-21
    Description: Fonction pour retourner la page famille.
    """
    if request.method == 'GET':
        nomFamilleId = request.user.individu.famille.id
    elif request.method == 'POST':
        nomFamille = request.POST['nomFamilleRecherche']
        nomFamilleId = nomFamille.split('#')[-1]
        nomFamilleId = int(nomFamilleId)
    try:
        # Récupère le lien de parenté
        nomRechercheFamille = Famille.objects.get(id=nomFamilleId)
        individus = Individu.objects.all()
        liens = Nom_Lien_Parente.objects.all()
        lienParents = nomRechercheFamille.lien_parente_set.all()
        if not lienParents:
            return render(request, 'mainapp/famille.html', locals())
        lienParents = list(lienParents)
        lienParents = triListeAge(lienParents)
        arbre = creationListe(lienParents)
        arbre = triListeListeAge(arbre)
        arbre = makeFirstChild(arbre)
        arbre = rechercheParent(arbre)
        arbre = creationArbre(arbre, 0, [], 0)
        arbre = [arbre]
        arbre = json.dumps(arbre)
        return render(request, 'mainapp/famille.html', locals())
    except:
        messages.add_message(request, messages.ERROR, "La famille que vous recherchez n'existe pas.")
        return HttpResponseRedirect(reverse('accueil'))

# Fin Creation Arbre


@csrf_exempt
@login_required
@permission_required("mainapp.admin_famille")
def editfamille(request):
    """
    File: famille.py
    Author: Antoine Bourgeois
    Email: bourgeoisa@eisti.eu
    Date: 2016-12-21
    Description: Fonction pour modifié  la famille.
    """
    f = request.user.individu.famille
    users = [individu.user for individu in f.individu_set.all()]
    photo = request.user.individu.famille.photo
    if request.method == 'POST':
        post = request.POST['username']
        user_id = json.loads(post)
        content_type = ContentType.objects.get_for_model(Individu)
        permission = Permission.objects.get(content_type=content_type, codename='admin_famille')
        user = User.objects.get(id=user_id)
        if user.has_perm('mainapp.admin_famille'):
            user.user_permissions.remove(permission)
        else:
            user.user_permissions.add(permission)
        user.save()
        json_data = json.dumps({"HTTPRESPONSE": user_id})
        return HttpResponse(json_data)
    return render(request, 'mainapp/editfamille.html', {'users': users, 'photo': photo})


@csrf_exempt
@login_required
@permission_required("mainapp.admin_famille")
def updatefamille(request):
    """
    File: famille.py
    Author: Antoine Bourgeois
    Email: bourgeoisa@eisti.eu
    Date: 2016-12-21
    Description: Fonction pour sauvegarder la nouvelle famille.
    """
    if request.method == 'POST':
        post = request.POST['id_famille']
        post2 = request.POST['update_nom_famille']
        idfamille = json.loads(post)
        newfamille = json.loads(post2)
        famille = Famille.objects.get(id=idfamille)
        famille.nom = newfamille
        famille.save()
        json_data = json.dumps({"HTTPRESPONSE": 'fxd'})
        return HttpResponse(json_data)
    else:
        return HttpResponseNotFound('<h1>Page not found</h1>')


@login_required
@permission_required("mainapp.admin_famille")
def upload_pic(request):
    """
    File: famille.py
    Author: Antoine Bourgeois
    Email: bourgeoisa@eisti.eu
    Date: 2016-12-21
    Description: Fonction pour ajouter une photo à un membre de la famille.
    """
    if request.method == 'POST':
        max_upload_size = 2621440
        form = ImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            f = request.user.individu.famille
            photo_upload = form.cleaned_data['photo']
            if photo_upload.size <= max_upload_size:
                photo_upload.name = str(request.user.individu.famille.id) + '.' + photo_upload.name.split('.')[-1]
                if request.user.individu.famille.photo.name != 'famille/default.png':
                    request.user.individu.famille.photo.delete()
                f.photo = photo_upload
                f.save()
            else:
                messages.add_message(request, messages.ERROR, "L'image importée est trop lourde.")
        else:
            messages.add_message(request, messages.ERROR, "Le fichier importé n'est pas une image.")
        return HttpResponseRedirect(reverse('editfamille'))
    return HttpResponseNotFound('Allowed only via POST')


@login_required
@permission_required("mainapp.admin_famille")
def accepterMembre(request):
    """
    File: famille.py
    Author: Antoine Bourgeois
    Email: bourgeoisa@eisti.eu
    Date: 2016-12-21
    Description: Fonction pour accepter un membre dans la famille
    """
    if request.method == 'POST':
        form = MembreForm(request.POST)
        user_id = form.data['id_user']
        content_type = ContentType.objects.get_for_model(Individu)
        permission = Permission.objects.get(content_type=content_type, codename='confirmation')
        user = User.objects.get(id=user_id)
        user.user_permissions.remove(permission)
        return HttpResponseRedirect(reverse('editfamille'))
    return HttpResponseNotFound('Allowed only via POST')


@login_required
@permission_required("mainapp.admin_famille")
def refuserMembre(request):
    """
    File: famille.py
    Author: Antoine Bourgeois
    Email: bourgeoisa@eisti.eu
    Date: 2016-12-21
    Description: Fonction pour refuser d'ajouter un membre dans la famille.
    """
    if request.method == 'POST':
        form = MembreForm(request.POST)
        user_id = form.data['id_user']
        content_type = ContentType.objects.get_for_model(Individu)
        permission = Permission.objects.get(content_type=content_type, codename='confirmation')
        user = User.objects.get(id=user_id)
        user.user_permissions.remove(permission)
        f = Famille.objects.get(nom=user.individu.famille)
        f.individu_set.remove(user.individu)
        return HttpResponseRedirect(reverse('editfamille'))
    return HttpResponseNotFound('Allowed only via POST')


@login_required
def ajoutLienParente(request):
    """
    File: famille.py
    Author: Antoine Bourgeois
    Email: bourgeoisa@eisti.eu
    Date: 2016-12-21
    Description: Fonction pour ajouter un lien de parenté entre deux individus.
    """
    if request.method == 'POST':
        form = AjoutLienParenteForm(request.POST)
        if form.is_valid():
            ind1 = form.data['ind1']
            ind2 = form.data['ind2']
            lien = form.data['lien']
            try:
                individu1 = Individu.objects.get(id=ind1)
                individu2 = Individu.objects.get(id=ind2)
                lien = Nom_Lien_Parente.objects.get(id=lien)
                Lien_Parente(famille=individu1.famille, individu1=individu1, individu2=individu2, nom_lien_parente=lien).save()
            except IntegrityError:
                return HttpResponseRedirect(reverse('famille'))

        return HttpResponseRedirect(reverse('famille'))
    return HttpResponseNotFound('Allowed only via POST')
