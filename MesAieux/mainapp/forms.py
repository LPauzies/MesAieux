from django import forms


class InscriptionForm(forms.Form):
    nom = forms.CharField(
        max_length=30,
        widget=forms.TextInput(attrs={'class': "field", 'placeholder': "Nom"}),
        label='Nom'
    )
    prenom1 = forms.CharField(
        max_length=30,
        widget=forms.TextInput(attrs={'placeholder': 'Premier prénom'}),
        label="Premier prénom"
    )
    prenom2 = forms.CharField(
        max_length=30,
        widget=forms.TextInput(attrs={'placeholder': 'Deuxième prénom'}),
        label="Deuxième prénom",
        required=False
    )
    prenom3 = forms.CharField(
        max_length=30,
        widget=forms.TextInput(attrs={'placeholder': 'Troisième prénom'}),
        label="Troisième prénom",
        required=False
    )
    email = forms.EmailField(widget=forms.TextInput(attrs={'placeholder': 'exemple@mail.fr'}))
    password = forms.CharField(widget=forms.PasswordInput, required="required")
    password_conf = forms.CharField(widget=forms.PasswordInput, required="required")
    CHOICES = (('homme', 'homme'), ('femme', 'femme'),)
    genre = forms.ChoiceField(choices=CHOICES)
    nais = forms.DateField(label="Date de naissance (jj/mm/aaaa)")
    mariage = forms.DateField(label="Date de mariage (jj/mm/aaaa)", required=False)
    nationalite = forms.CharField(label="Nationalité")
    occupation = forms.CharField(label="Occupation Actuelle", max_length=100, required=False, widget=forms.TextInput(attrs={'placeholder': 'Décrivez votre occupation actuelle en 100 caractères max'}))
    numero = forms.CharField(label="Numéro de rue", max_length=10, required=False)
    nomrue = forms.CharField(label="Nom de rue", max_length=100, required=False)
    ville = forms.CharField(label="Ville", max_length=50, required=False)
    code = forms.CharField(label="Code Postal", max_length=5, required=False)
    telephone = forms.CharField(label="Numéro de téléphone", max_length=10, required=False)


class ConnexionForm(forms.Form):
    user = forms.EmailField(label="Adresse mail")
    pwd = forms.CharField(label="Mot de passe", widget=forms.PasswordInput)


class CreerfamilleForm(forms.Form):
    nom = forms.CharField(label="Nom de la famille", max_length=30)


class ModifForm(forms.Form):
    nom = forms.CharField(
        max_length=30,
        widget=forms.TextInput(attrs={'class': "field", 'value': "Voir BDD", 'disabled': ""}),
        label='Nom'
    )
    prenom1 = forms.CharField(
        max_length=30,
        widget=forms.TextInput(attrs={'value': "Voir BDD", 'disabled': ""}),
        label="Premier prénom"
    )
    prenom2 = forms.CharField(
        max_length=30,
        widget=forms.TextInput(attrs={'placeholder': 'Deuxième prénom'}),
        label="Deuxième prénom",
        required=False
    )
    prenom3 = forms.CharField(
        max_length=30,
        widget=forms.TextInput(attrs={'placeholder': 'Troisième prénom'}),
        label="Troisième prénom",
        required=False
    )
    email = forms.EmailField(
        widget=forms.TextInput(attrs={'value': 'exemple@BDD.fr'}),
        required=False
    )
    mariage = forms.DateField(
        widget=forms.TextInput(attrs={'value': 'jj/mm/aaaa'}),
        label="Date de mariage (jj/mm/aaaa) (Indiquez la plus récente si c'est le cas)",
        required=False
    )
    nationalite = forms.CharField(label="Nationalité")
    occupation = forms.CharField(
        label="Occupation Actuelle",
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={'value': 'Voir BDD'})
    )
    numero = forms.CharField(
        label="Numéro",
        max_length=10,
        required=False,
        widget=forms.TextInput(attrs={'value': 'Voir BDD'})
    )
    nomrue = forms.CharField(
        label="Nom",
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={'value': 'Voir BDD'})
    )
    ville = forms.CharField(
        label="Ville",
        max_length=50,
        required=False,
        widget=forms.TextInput(attrs={'value': 'Voir BDD'})
    )
    code = forms.CharField(
        label="Code Postal",
        max_length=5,
        required=False,
        widget=forms.TextInput(attrs={'value': 'BDD'})
    )
    telephone = forms.CharField(
        label="Numéro de téléphone",
        max_length=10,
        required=False,
        widget=forms.TextInput(attrs={'value': 'Voir BDD'})
    )
    hidden_address = forms.BooleanField(
        label="Voulez vous cacher vos coordonnées ?",
        required=False
    )
    hidden_telephone = forms.BooleanField(
        label="Voulez vous cacher votre numéro de téléphone ?",
        required=False
    )


class ImageUploadForm(forms.Form):
    photo = forms.ImageField()


class MembreForm(forms.Form):
    id_user = forms.CharField(max_length=10)


class MessageForm(forms.Form):
    destinataire = forms.CharField(max_length=100)
    message = forms.CharField(
        max_length=300,
        widget=forms.TextInput()
    )


class DocumentForm(forms.Form):
    commentaire = forms.CharField(
        max_length=300,
        widget=forms.TextInput()
    )
    tag1 = forms.CharField(max_length=20, required=False)
    tag2 = forms.CharField(max_length=20, required=False)
    tag3 = forms.CharField(max_length=20, required=False)
    doc = forms.FileField()


class ValidationDocumentForm(forms.Form):
    id_document = forms.CharField(max_length=10)


class RechercheForm(forms.Form):
    prenom = forms.CharField(max_length=50, required=False)
    nom = forms.CharField(max_length=50, required=False)
    nationalite = forms.CharField(max_length=50, required=False)
    naissance = forms.DateField(required=False)
    mariage = forms.DateField(required=False)
    deces = forms.DateField(required=False)


class RechercheDocumentsForm(forms.Form):
    tag1 = forms.CharField(max_length=10, required=False)
    tag2 = forms.CharField(max_length=10, required=False)
    tag3 = forms.CharField(max_length=10, required=False)


class AjoutLienParenteForm(forms.Form):
    ind1 = forms.CharField(max_length=100, required=True)
    ind2 = forms.CharField(max_length=100, required=True)
    lien = forms.CharField(max_length=100, required=True)
