from django.conf.urls import url

from . import views

urlpatterns = [
    # Page permettant l'inscription
    url(r'^inscription/$', views.inscription, name="inscription"),
    # Page permettant la connexion
    url(r'^connexion/$', views.connexion, name="connexion"),

    # INDIVIDU
    # Page permettant d'acceder à ses information
    url(r'^moncompte/$', views.moncompte, name="moncompte"),
    # Page permettant de se logout
    url(r'^logout/$', views.logout_view, name='logout'),
    # Page permettant de modifier sa photo de profil
    url(r'^profilpic/$', views.upload_pic_user, name='profilpic'),
    # Page permettant de modifier son mot de passe
    url(r'^getpwd/$', views.getPassword, name='getpwd'),

    # FAMILLES
    # Page permettant de creer un famille
    url(r'^creerfamille/$', views.creerfamille, name='creerfamille'),
    # Page permettant de mettre à jour le nom d'une famille
    url(r'^updatefamille/$', views.updatefamille, name='updatefamille'),
    # Page permettant de rejoindre une famille déjà existante
    url(r'^rejoindreFamille/$', views.rejoindreFamille, name='rejoindreFamille'),
    # Page permettant de modifier un famille et ses membres
    url(r'^editfamille/$', views.editfamille, name='editfamille'),
    # Page permettant de modifier la photo d'une famille
    url(r'^famillepic/$', views.upload_pic, name='famillepic'),
    # Page permettant d'accepter un membre dans sa famille
    url(r'^accepterMembre/$', views.accepterMembre, name='accepterMembre'),
    # Page permettant de refuser un membre dans sa famille
    url(r'^refuserMembre/$', views.refuserMembre, name='refuserMembre'),
    # Page permettant d'ajouter la date de décès d'un individu
    url(r'^ajoutDateDeces/$', views.ajoutDateDeces, name='ajoutDateDeces'),
    # Url permettant d'ajouter un lien de parente
    url(r'^ajoutLienParente/$', views.ajoutLienParente, name='ajoutLienParente'),

    # ARBRE
    url(r'^famille/$', views.famille, name='famille'),

    # MESSAGES
    # Page permettant d'acceder à ses messages
    url(r'^Messages/$', views.message, name='message'),
    # Page permettant de supprimer ses messages
    url(r'^supprimermessage/$', views.supprimer_message, name='supprimermessage'),

    # DOCUMENTS
    # Page permettant d'accéder à l'interface historien
    url(r'^historien/$', views.historien, name='historien'),
    # Page permettant d'accéder à l'interface d'upload de document
    url(r'^ajoutdocuments/$', views.upload_file, name='ajoutdocuments'),
    # Page permettant de visualiser ses documents
    url(r'^documents/$', views.individu_files, name='documents'),
    # Page permettant de valider un document
    url(r'^accepterDocument/$', views.accepterDocument, name='accepterDocument'),
    # Page permettant à un historien de modifier un document
    url(r'^modifierDocument/$', views.modifierDocument, name='modifierDocument'),
    # Page permettant de refuser un document
    url(r'^refuserDocument/$', views.refuserDocument, name='refuserDocument'),
    # Page permettant de rechercher un document
    url(r'^rechercheDocuments/$', views.rechercheDocuments, name='rechercheDocuments'),

    # AUTRES
    # Page permettant de voir les mentions legales
    url(r'^mentionslegales/$', views.mentionslegales, name='mentionslegales'),
    # Page permettant de voir les contacts du site
    url(r'^contact/$', views.contact, name='contact'),
    # Page d'accueil
    url(r'^$', views.accueil, name="accueil"),
    # Page de recherche
    url(r'^recherche/$', views.recherche, name="recherche"),
]
