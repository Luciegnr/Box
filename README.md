# Box

## Installation du projet 


Nous nous plaçons dans le répertoire /home/'utilisateur' pour cloner notre projet.
* cd /home/'utilisateur'
* git clone git@rendu-git.etna-alternance.net:module-8034/activity-43945/group-870418 UNI2

Nous installons pip3 afin de pouvoir installer les librairies utilisées dans notre script. 
`sudo apt install python3-pip`

Puis nous installons PyYaml à l'aide de pip3 qui est une bibliothèque python nous servant pour analyser le fichier .yaml
`sudo pip3 install pyyaml`


Afin de rendre fonctionnel notre projet il est nécessaire de faire deux  modifications dans le cas où votre utilisateur ne serait pas "box" comme dans notre script. Il faut donc se rendre dans le fichier: `/home/'utilisateur'/UNI2/box/box/script.py`
* cd /home/'utilisateur'/UNI2/box/box
* emacs script.py

Et modifier dans notre fonction `install` la ligne suivante:
```
def install():
    with open("/home/box/UNI2/box/box/mongo.yml", "r") as ymlfile:
```
et changer dans `/home/'utilisateur'/UNI2/box/box/mongo.yml`le premier "box" par le nom de votre utilisateur.


Le deuxième changement se réalise dans le fichier suivant permettant de créer notre package:
* cd /home/'utilisateur'/UNI2/box
* emacs setup.py

Il faut alors modifier cette ligne:
`scripts=['/home/box/UNI2/box/box/script.py'],`
En changeant encore une fois le premier "box" dans `/home/box/UNI2/box/box/script.py` par le nom de votre utilisateur.


Une fois ces changements réallisés il vous ait normalement possible de télécharger notre package en éxecutant les commandes suivantes: 
* sudo pip3 install build && sudo python3 setup.py sdist && sudo pip3 install wheel && sudo python3 setup.py build && sudo python3 setup.py install && sudo pip3 install dist/box-0.1.0.tar.gz

Il y a maintenant trois commandes qui ont été créées afin de lancer notre programme, la première:`sudo box init` nous permet de préparer notre environnement avec la création du système de fichier de la base debian dans le dossier /var/lib/box/base/. Notre script gère le téléchargement de l'archive et son unzip ainsi que les cas d'erreur de mount et de création des dossiers.

La deuxième commande est: `sudo box build mongo.yml` celle ci nous permet de récupérer les commandes d'installation de mongodb contenues dans notre fichier mongo.yml et de changer le dossier racine où les commande d'installation de mongodb sont executées grâce à un `chroot /var/lib/box/env/mongodb`
C'est ainsi que nous créons notre environnement.

Et pour finir, la commande `sudo box run mongodb` nous permet tout simplement de lancer notre environnement soit ici mongodb.