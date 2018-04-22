from django.shortcuts import render
from django.contrib import messages
from django.http import HttpResponseNotFound, HttpResponseRedirect, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.urls import reverse
from django.contrib.auth.decorators import login_required, permission_required
import json

from mainapp.forms import DocumentForm, ValidationDocumentForm, RechercheDocumentsForm
from mainapp.models import Banque


@login_required
@permission_required("mainapp.historien")
def historien(request):
    """
    File: documents.py
    Author: Laurine Sorel
    Email: sorellauri@eisti.eu
    Description: Récupère tout les documents non validé
    Date: 20/12/2016
    """
    documents = Banque.objects.filter(validation=False)
    return render(request, 'mainapp/historien.html', {"documents": documents})


@login_required
@permission_required("mainapp.historien")
def accepterDocument(request):
    """
    File: documents.py
    Author: Laurine Sorel
    Email: sorellauri@eisti.eu
    Description: Valide le document envoyé
    Date: 20/12/2016
    """
    if request.method == 'POST':
        form = ValidationDocumentForm(request.POST)
        id_document = form.data['id_document']
        doc = Banque.objects.get(id=id_document)
        doc.validation = True
        doc.save()
        return HttpResponseRedirect(reverse('historien'))
    return HttpResponseNotFound('Allowed only via POST')


@csrf_exempt
@login_required
@permission_required("mainapp.historien")
def modifierDocument(request):
    """
    File: documents.py
    Author: Laurine Sorel
    Email: sorellauri@eisti.eu
    Description: Ajoute le données de l'historien
    Date: 21/12/2016
    """
    if request.method == "POST":
        post1 = request.POST['id_document']
        post2 = request.POST['annotation']
        post3 = request.POST['date']
        id_document = json.loads(post1)
        annotation = json.loads(post2)
        date = json.loads(post3)
        doc = Banque.objects.get(id=id_document)
        doc.comHistorien = annotation
        doc.dateHistorien = date
        doc.save()
        json_data = json.dumps({"date": date, "annotation": annotation})
        return HttpResponse(json_data)


@login_required
@permission_required("mainapp.historien")
def refuserDocument(request):
    """
    File: documents.py
    Author: Laurine Sorel
    Email: sorellauri@eisti.eu
    Description: Supprime le document invalidé
    Date: 20/12/2016
    """
    if request.method == 'POST':
        form = ValidationDocumentForm(request.POST)
        id_document = form.data['id_document']
        doc = Banque.objects.get(id=id_document)
        doc.delete()
        return HttpResponseRedirect(reverse('historien'))
    return HttpResponseNotFound('Allowed only via POST')


@login_required
def upload_file(request):
    """
    File: documents.py
    Author: Laurine Sorel
    Email: sorellauri@eisti.eu
    Description: Fonction permettant d'enregistrer un fichier dans la base de données
    """
    if request.method == 'POST':
        max_upload_size = 5242880
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            doc = form.cleaned_data['doc']
            tag1 = form.cleaned_data['tag1']
            tag2 = form.cleaned_data['tag2']
            tag3 = form.cleaned_data['tag3']
            commentaire = form.cleaned_data['commentaire']
            if doc.size <= max_upload_size:
                Banque(individu=request.user.individu, fichier=doc, commentaire=commentaire, tag=tag1 + " " + tag2 + " " + tag3).save()
                messages.add_message(request, messages.SUCCESS, "Le fichier a bien été enregistré. Il est en attente de validation par un de nos historiens ...")
            else:
                messages.add_message(request, messages.ERROR, "Le fichier importé est trop lourd !")
        else:
            messages.add_message(request, messages.ERROR, "Le formulaire a été mal rempli. Veuillez réessayer ...")
    return render(request, 'mainapp/ajoutdocuments.html', locals())


@login_required
def individu_files(request):
    """
    File: documents.py
    Author: sorellauri
    Email: sorellauri@eisti.eu
    Description: Fonction permettant de retourner tout les fichiers d'un individu
    """
    files = request.user.individu.banque_set.all()
    return render(request, 'mainapp/documents.html', {"files": files})


def rechercheDocuments(request):
    """
    File: documents.py
    Author: Laurine Sorel
    Email: sorellauri@eisti.eu
    Description: Fonction permettant de rechercher un document selon plusieurs paramètres
    Date: 23/12/2016
    """
    if request.method == "POST":
        form = RechercheDocumentsForm(request.POST)
        if form.is_valid():
            key1 = form.data['tag1']
            key2 = form.data['tag2']
            key3 = form.data['tag3']
            if key1 or key2 or key3:
                recherche = Banque.objects
                if key1:
                    recherche = recherche.filter(tag__icontains=key1)
                if key2:
                    recherche = recherche.filter(tag__icontains=key2)
                if key3:
                    recherche = recherche.filter(tag__icontains=key3)
                messages.add_message(request, messages.SUCCESS, "Recherche : " + key1 + " " + key2 + " " + key3)
                return render(request, 'mainapp/rechercheDocuments.html', {"rechercher": recherche})
            else:
                messages.add_message(request, messages.ERROR, "Aucun champs n'a été saisi !")
        else:
            messages.add_message(request, messages.ERROR, "Les données saisies ne correspondent pas au format requis")
    return render(request, 'mainapp/rechercheDocuments.html')
