from django.contrib import admin
from .models import Individu, Famille, Coordonnee, Nom_Lien_Parente, Lien_Parente, Banque, Message


class IndividuAdmin(admin.ModelAdmin):
    list_display = ('user', 'famille', 'prenom2', 'nationalite')


class CoordonneeAdmin(admin.ModelAdmin):
    list_display = ('user', 'nomrue', 'ville', 'code', 'telephone')


class ConnexionAdmin(admin.ModelAdmin):
    list_display = ('individu', 'email')


class Lien_ParenteAdmin(admin.ModelAdmin):
    list_display = ('famille', 'individu1', 'individu2', 'nom_lien_parente')


class MessageAdmin(admin.ModelAdmin):
    list_display = ('message', 'user1', 'user2')


class BanqueAdmin(admin.ModelAdmin):
    list_display = ('individu', 'commentaire', 'tag')


admin.site.register(Individu, IndividuAdmin)
admin.site.register(Famille)
admin.site.register(Coordonnee, CoordonneeAdmin)
admin.site.register(Message, MessageAdmin)
admin.site.register(Nom_Lien_Parente)
admin.site.register(Lien_Parente, Lien_ParenteAdmin)
admin.site.register(Banque, BanqueAdmin)
