import json
from django.shortcuts import render
from django.contrib.auth.models import User, Permission
from django.db import IntegrityError
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse, HttpResponseNotFound
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.contenttypes.models import ContentType

from mainapp.forms import InscriptionForm, ConnexionForm, ModifForm, ImageUploadForm
from mainapp.models import Individu, Coordonnee


def checkDate_naissance(date_str):
    """
    File: individu.py
    Author: Lucas Pauzies
    Email: pauziesluc@eisti.eu
    Date: 2016-12-08
    Description: Prédicat de date. Renvoi True si une date est valide et de la forme "jj/mm/yyyy", False sinon.
    """
    # date_str = chaine de date à vérifier "jj/mm/yyyy"
    import datetime
    import re
    # On teste si la chaine à la bonne structure.
    pattern = re.compile("^[0-9]{2}/[0-9]{2}/[0-9]{4}$")
    correctDate = False
    if pattern.match(date_str):
        tab_date = date_str.split('/')
        # [0] = jj; [1] = mm; [2] = yyyy
        try:
            datetime.datetime(int(tab_date[2]), int(tab_date[1]), int(tab_date[0]))
            correctDate = True
        except ValueError:
            correctDate = False
    return correctDate


def checkDate_mariage(date_str):
    """
    File: individu.py
    Author: Lucas Pauzies
    Email: pauziesluc@eisti.eu
    Date: 2016-12-08
    Description: Prédicat de date. Renvoi True si une date est valide et de la forme "jj/mm/yyyy" ou "", False sinon.
    """
    # date_str = chaine de date à vérifier "jj/mm/yyyy"
    import datetime
    import re
    # On teste si la chaine à la bonne structure.
    pattern = re.compile("^[0-9]{2}/[0-9]{2}/[0-9]{4}$")
    correctDate = False
    if (date_str == ""):
        correctDate = True
        return correctDate
    elif pattern.match(date_str):
        tab_date = date_str.split('/')
        # [0] = jj; [1] = mm; [2] = yyyy
        try:
            datetime.datetime(int(tab_date[2]), int(tab_date[1]), int(tab_date[0]))
            correctDate = True
        except ValueError:
            correctDate = False
        return correctDate
    else:
        return correctDate


def inscription(request):
    """
    File: views.py
    Author: Laurine Sorel
    Email: sorellauri@eisti.eu
    Date: 2016-11-04
    Description: Fonction permettant la vérification des champs du formulaire d'inscription et l'enregistrement des données vérifiées dans la base de donnée
    """
    # Vérifie si l'utilisateur n'est pas déjà connecté
    if not request.user.is_authenticated:
        # Vérifie si les données passé se font en POST
        if request.method == 'POST':
            # Appelle la fonction InscriptionForm afin de passer le formulaire à l'utilisateur
            form = InscriptionForm(request.POST)
            # Si le formulaire est valide
            if form.is_valid():
                try:
                    # Récupération des données nécessaires
                    nom = form.data['nom']
                    prenom1 = form.data['prenom1']
                    newprenom2 = form.data['prenom2']
                    newprenom3 = form.data['prenom3']
                    email = form.data['email']
                    password = form.data['password']
                    password_conf = form.data['password_conf']
                    newgenre = form.data['genre']
                    newnais = form.data['nais']
                    newmariage = form.data['mariage']
                    # Récupère les données relative à la nationalité
                    newnationalite = form.data['nationalite'].split(">")[2]
                    newoccupation = form.data['occupation']
                    newnumero = form.data['numero']
                    newnomrue = form.data['nomrue']
                    newville = form.data['ville']
                    newcode = form.data['code']
                    newtelephone = form.data['telephone']
                    bool_nais = checkDate_naissance(newnais)
                    bool_mariage = checkDate_mariage(newmariage)
                    # Seulement si la date de naissance est une date valide et la date de mariage et valide ou vide
                    if (bool_nais and bool_mariage):
                        # Création et enregistrement de l'individu dans la table user
                        # Seulement si le mot de passe de l'individu est matché avec sa confirmation
                        if (password == password_conf):
                            newuser = User.objects.create_user(email, email, password)
                            newuser.first_name = prenom1
                            newuser.last_name = nom
                            # Écriture dans la base de donnée du user créer ci-dessus
                            newuser.save()
                            # Écriture dans la table Individu les informations du user
                            Individu(user=newuser, prenom2=newprenom2, prenom3=newprenom3, genre=newgenre, date_nais=newnais, date_mariage=newmariage, nationalite=newnationalite, occupation=newoccupation).save()
                            # Écriture dans la table Coordonnee les informations du user
                            Coordonnee(user=newuser, numero=newnumero, nomrue=newnomrue, ville=newville, code=newcode, telephone=newtelephone).save()
                            content_type = ContentType.objects.get_for_model(Coordonnee)
                            permission_address = Permission.objects.get(content_type=content_type, codename='hidden_address')
                            newuser.user_permissions.add(permission_address)
                            permission_telephone = Permission.objects.get(content_type=content_type, codename='hidden_telephone')
                            newuser.user_permissions.add(permission_telephone)
                            newuser.save()
                            messages.add_message(request, messages.INFO, 'Vous êtes bien inscrit ! Bienvenue sur Mes Aieux !')
                            login(request, newuser)
                            return HttpResponseRedirect(reverse('accueil'))
                        else:
                            # On indique l'erreur à l'utilisateur via message (mot de passe confirmation)
                            messages.add_message(request, messages.ERROR, "Vous n'avez pas bien confirmé votre mot de passe")
                            return HttpResponseRedirect(reverse('inscription'))
                    else:
                        # On indique l'erreur à l'utilisateur via message (date de naissance ou mariage)
                        messages.add_message(request, messages.ERROR, "Vous n'avez pas bien rentré les dates du formulaire")
                        return HttpResponseRedirect(reverse('inscription'))
                except IntegrityError:
                    # Si le formulaire n'est pas rempli correctement, une erreur est généré et le formulaire renvoyé à l'utilisateur
                    messages.add_message(request, messages.ERROR, "Erreur d'intégrité")
                    return HttpResponseRedirect(reverse('inscription'))
            else:
                # Si le formulaire n'est pas rempli correctement, une erreur est généré et le formulaire renvoyé à l'utilisateur
                messages.add_message(request, messages.ERROR, "Le formulaire ne respecte pas les caractéristiques des champs")
                return HttpResponseRedirect(reverse('inscription'))
        else:
            # On renvoie le formulaire d'inscription vide
            form = InscriptionForm()
    else:
        # Si le user est déjà connecté il est redirigé vers sa page de compte
        return HttpResponseRedirect(reverse('moncompte'))

    return render(request, 'mainapp/inscription.html', locals())


def connexion(request):
    """
    File: views.py
    Author: Laurine Sorel
    Email: sorellauri@eisti.eu
    Date: 2016-11-04
    Description: Fonction permettant la connexion d'un user
    """
    # Si le user n'est pas déjà connecté
    if not request.user.is_authenticated:
        if request.method == 'POST':
            # Appelle du formulaire de connexion
            form = ConnexionForm(request.POST)
            # Si le formulaire est valide
            if form.is_valid():
                try:
                    # Tentative de connexion du user
                    user = authenticate(username=form.data['user'], password=form.data['pwd'])
                    if user is not None:
                        login(request, user)
                        erreur = "Connexion valide"
                        return HttpResponseRedirect(reverse('moncompte'))
                    else:
                        messages.add_message(request, messages.ERROR, 'Identifiant ou mot de passe invalide', fail_silently=True)
                except IntegrityError:
                    messages.add_message(request, messages.ERROR, 'Identifiant ou mot de passe invalide')
        else:
            form = ConnexionForm()
    else:
        return HttpResponseRedirect(reverse('moncompte'))
    return render(request, 'mainapp/connexion.html', locals())


def logout_view(request):
    """
    File: views.py
    Author: Laurine Sorel
    Email: sorellauri@eisti.eu
    Date: 2016-11-04
    Description: Fonction permettant au user de se déconnecter
    """
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('inscription'))
    else:
        logout(request)
        messages.add_message(request, messages.SUCCESS, 'Vous avez bien été déconnecté, merci à vous !')
    return HttpResponseRedirect(reverse('accueil'))


@login_required(login_url='/connexion/')
def moncompte(request):
    """
    File: individu.py
    Author: Lucas Pauzies
    Email: pauziesluc@eisti.eu
    Date: 2016-11-08
    Description: Fonction de modification des données et de visualisation de celles-ci
    """
    # Pas besoin de vérifier l'authetification car le user est supposé être déjà connecté
    if request.method == 'POST':
        # messages.add_message(request, messages.INFO, 'Fonctionnalité pas encore implémentée')
        # Appelle la fonction ModifForm afin de passer le formulaire à l'utilisateur
        form = ModifForm(request.POST)
        # Si il est valide
        if form.is_valid():
            # Récupération des données nécessaires
            newprenom2 = form.data['prenom2']
            newprenom3 = form.data['prenom3']
            newmariage = form.data['mariage']
            bool_mariage = checkDate_mariage(newmariage)
            # Récupère les données relative à la nationalité
            newnationalite = form.data['nationalite'].split('>')[2]
            newoccupation = form.data['occupation']
            newnumero = form.data['numero']
            newnomrue = form.data['nomrue']
            newville = form.data['ville']
            newcode = form.data['code']
            newtelephone = form.data['telephone']
            if bool_mariage:
                bool_hidden_address = request.POST.get('hidden_address', False)
                # si la checkbox adresse est checked renvoi "hidden_address" sinon renvoi False
                bool_hidden_telephone = request.POST.get('hidden_telephone', False)
                # si la checkbox telephone est checked renvoi "hidden_telephone" sinon renvoi False
                content_type = ContentType.objects.get_for_model(Coordonnee)
                if bool_hidden_address:  # si cochée j'attribue la permission adresse
                    permission_address = Permission.objects.get(content_type=content_type, codename='hidden_address')
                    request.user.user_permissions.add(permission_address)
                    request.user.save()
                else:  # sinon je retire la permissionadresse
                    permission_address = Permission.objects.get(content_type=content_type, codename='hidden_address')
                    request.user.user_permissions.remove(permission_address)
                    request.user.save()
                if bool_hidden_telephone:  # si cochée j'attribue la permission telephone
                    permission_address = Permission.objects.get(content_type=content_type, codename='hidden_telephone')
                    request.user.user_permissions.add(permission_address)
                    request.user.save()
                else:  # sinon je retire la permission telephone
                    permission_address = Permission.objects.get(content_type=content_type, codename='hidden_telephone')
                    request.user.user_permissions.remove(permission_address)
                    request.user.save()
                # On met à jour la BDD !
                request.user.individu.prenom2 = newprenom2
                request.user.individu.prenom3 = newprenom3
                request.user.individu.date_mariage = newmariage
                request.user.individu.nationalite = newnationalite
                request.user.individu.occupation = newoccupation
                request.user.coordonnee.numero = newnumero
                request.user.coordonnee.nomrue = newnomrue
                request.user.coordonnee.ville = newville
                request.user.coordonnee.code = newcode
                request.user.coordonnee.telephone = newtelephone
                request.user.individu.save()
                request.user.coordonnee.save()
                messages.add_message(request, messages.SUCCESS, 'Votre profil a été mis à jour')
            else:
                messages.add_message(request, messages.ERROR, "La date de mariage rentrée est invalide")
        else:
            messages.add_message(request, messages.ERROR, "Vous n'avez pas rempli le formulaire correctement")
        return HttpResponseRedirect(reverse('moncompte'))
    else:
        form = ModifForm()
        return render(request, 'mainapp/moncompte.html', locals())


@csrf_exempt
@login_required
def getPassword(request):
    """
    File: individu.py
    Author: Lucas Pauzies
    Email: pauziesluc@eisti.eu
    Date: 2016-11-09
    Description: Fonction de modification du mot de passe
    """
    if request.method == 'POST':
        old = json.loads(request.POST['old_password'])
        new = json.loads(request.POST['new_password'])
        con = json.loads(request.POST['con_password'])
        # old_bdd = request.user.password  # Ancien mot de passe encodé
        if request.user.check_password(old):
            # Si le mot de passe à changer est correct
            if (new == con):
                # Si le mot de passe nouveau est pas matché
                if (len(new) >= 8):
                    # Si le mot de passe nouveau est supérieur à 8 caractères
                    request.user.set_password(new)
                    # On change le mot de passe dans la BDD
                    request.user.save()
                    login(request, request.user)
                    # On sauvegarde la BDD
                    messages.add_message(request, messages.SUCCESS, 'Votre mot de passe à bien été changé !')
                else:
                    messages.add_message(request, messages.ERROR, 'Le mot de passe est trop court !')
            else:
                messages.add_message(request, messages.ERROR, 'Vous avez rentré deux mots de passe différents')
        else:
            messages.add_message(request, messages.ERROR, "Vous n'avez pas bien saisi votre mot de passe à changer")
        json_data = json.dumps({"HTTPRESPONSE": 'Password Changed'})
        return HttpResponse(json_data)
    else:
        return HttpResponseNotFound('<h1>Page not found</h1>')


@csrf_exempt
@login_required
def upload_pic_user(request):
    if request.method == 'POST':
        max_upload_size = 2621440
        form = ImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            photo_upload = form.cleaned_data['photo']
            if photo_upload.size <= max_upload_size:
                photo_upload.name = str(request.user.id) + '.' + photo_upload.name.split('.')[-1]
                if request.user.individu.photo.name != 'profil/default.png':
                    request.user.individu.photo.delete()
                request.user.individu.photo = photo_upload
                request.user.individu.save()
            else:
                messages.add_message(request, messages.ERROR, "L'image importée est trop lourde.")
        else:
            messages.add_message(request, messages.ERROR, "Le fichier importé n'est pas une image.")
        return HttpResponseRedirect(reverse('moncompte'))
    return HttpResponseNotFound('Allowed only via POST')


def check_date(date):
    """
    File: individu.py
    Author: Laurine Sorel
    Email: sorellauri@eisti.eu
    Description: Vérifie si le format d'une date est la bonne
    Date: 23/12/2016
    """
    import datetime
    try:
        datetime.datetime.strptime(date, '%d/%m/%Y')
        res = True
    except ValueError:
        res = False
    return res


@csrf_exempt
@login_required
@permission_required("mainapp.admin_famille")
def ajoutDateDeces(request):
    """
    File: individu.py
    Author: Laurine Sorel
    Email: sorellauri@eisti.eu
    Description: Ajout de la date de décès d'un individu
    Date: 23/12/2016
    """
    if request.method == "POST":
        id_individu = json.loads(request.POST['id_individu'])
        date = json.loads(request.POST['date'])
        if check_date(date):
            individu = Individu.objects.get(id=id_individu)
            individu.date_dece = date
            individu.save()
        json_data = json.dumps({"response": "Good"})
        return HttpResponse(json_data)
