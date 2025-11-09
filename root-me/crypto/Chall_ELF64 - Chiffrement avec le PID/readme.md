## Contexte et résumé du fonctionnement
Le binaire fourni vérifie si l'argument que tu lui donnes est égal au résultat de `crypt(str(PID), "$1$awesome")`, où :

- `PID` est l'ID du processus du programme (le processus du binaire `ch21` au moment de l'exécution),
- `"$1$awesome"` est le *salt* ; le préfixe `$1$` indique l'algorithme MD5-crypt,
- si le hash fourni en argument correspond exactement au hash du PID courant, le programme te donne un shell.

<img width="519" height="558" alt="image" src="https://github.com/user-attachments/assets/3705d6b7-a7ef-482a-b9c1-ee8578fee135" />

Le code en resume: 

Il transforme son PID en chaîne (par ex. "4567"). 

Il appelle crypt("4567", "$1$awesome") pour obtenir une sortie qui dépend du PID et du 
sel "awesome".

Le $1$ demande a la fonction crypt d’utiliser du MD5 

Il compare cette sortie à la valeur que tu as donnée en argument. 

Si tu as donné exactement le meme hash, alors il sait que ton argument correspond 
exactement au hash du PID de ce processus → il te donne un shell. 

Maintenant rapidement, pourquoi c est une vulnerabilité: Enfaite le programme utilise 
un “secret” qui est prévisible : le PID 

Donc enfaite comme le salt est fixe et que le pid est previsible bah le hash produit est 
completement déterministe 

Ce qu’on va faire: 

Logique: On va juste bruteforce en incrementant le PID jusqu’a tomber sur le bon 
Soit i un PID, on va faire: hash  = crypt(str(i), "$1$awesome") 
Puis ./ch21 hash 

On se connecte au chall en ssh: 

Une fois dans l’environnement on va se creer un fichier dans le dossier tmp 

<img width="604" height="164" alt="image" src="https://github.com/user-attachments/assets/387689fe-4de4-45a8-a11f-cbf5e382de0e" />

Petit script python: 

• import os, crypt : importe les modules os (pour obtenir le PID) et crypt (pour 
calculer le hash MD5-crypt). 

• pid_candidate = os.getpid() + 1 : récupère le PID du processus Python en cours 
et ajoute 1 (prévision du prochain PID). 

• print(crypt.crypt(str(pid_candidate), "$1$awesome")) : calcule et affiche le hash 
crypt("<pid+1>", "$1$awesome") (format MD5-crypt). 

Puis on rend le fichier executable avec chmod +x

Ensuite on test:

<img width="558" height="268" alt="image" src="https://github.com/user-attachments/assets/2e793329-5080-4169-84c7-92ce695916e4" />





