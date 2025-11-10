## Contexte
Retrouvez la clé de 12 caractères permettant de vous authentifier sur le service réseau.

Le titre est assez explicite il faut faire une timing attack

## Le principe

C’est une attaque qui consiste à deviner un secret en mesurant le temps que met le serveur à répondre à nos essais.

Le serveur compare très probablement la clé caractère par caractère et s’arrête dès qu’un caractère est faux.
Si on envoie une tentative, la durée entre notre envoi et la réponse du serveur dépend donc de jusqu’où le serveur a réussi la comparaison. 
En mesurant ce temps et en testant tous les caractères possibles à une position donnée, on peut deviner le caractère qui fait prendre le plus de temps au serveur : c’est probablement le bon. Répéter ceci pour chaque position permet de reconstruire la clé entière.

## Méthode que j’ai utilisée

Script python 

