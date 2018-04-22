# Mes Aïeux

## Authors :
- Antoine Bourgeois
- Romain Cayuela
- Lucas Pauzies
- Laurine Sorel

## Version :
Version 0.1

## Ref :
ING1-GL1-PROJET

## Description :
Création d'une application web permettant la création d'arbre généalogique.

## Version des outils et librairie utilisé
- Python 3
- Django 1.10.2
- Pillow

## Installation de l'environnement de développement (Pour les ordi de l'école)
- sudo apt-get install python3-pip
- sudo pip3 install virtualenvwrapper
- mkdir ~/.venv
- Ouvrir votre .bashrc / .zshrc / ... et y écrire :
    - WORKON_HOME="~/.venv" (Remplacer venv par la nom souhaité)
    - VIRTUALENVWRAPPER_PYTHON='/usr/bin/python3'
    - source /usr/local/bin/virtualenvwrapper.sh
- mkvirtualenv NomDeVotreVirtualEnv
- Pour basculer sur le virtualenv : workon NomDeVotreVirtualEnv
- Pour quitter le virtualenv : deactivate

## Installation de Django et des dépendances nécessaire
- Au niveau du fichier requirements.txt, dans le dossier GL_Project/MesAieux lancer la commande
    - pip install -r requirements.txt

## Lancement du serveur Django
- Au niveau du fichier manage.py, dans le dossier GL_Project/MesAieux lancer la commande
    - python3 manage.py runserver

## Calendrier des échéances :
| Description | Date de remise | Avancement |
|:---------------:|:--------------------:|:--------------------------:|
|Reformulation et Planning | 25 octobre 2016 | 100% |
|Base du code et fonctionnalités critiques | 13 novembre 2016 | 100% |
|Toutes les fonctionnalités | 18 décembre 2016 | 100 % |
|Rapport de synthèse et rapport technique | 6 janvier 2017 | 100% |
|Soutenance| 9-15 janvier 2016 | 100% |

## Organisation des pages
Voir le Wiki
