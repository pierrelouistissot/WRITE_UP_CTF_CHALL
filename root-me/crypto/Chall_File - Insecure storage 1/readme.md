## Contexte
Le challenge fournit une archive `ch20.tgz` contenant le dossier « navigateur » d’un utilisateur (profil Firefox). L’objectif est d’extraire et récupérer les mots de passe stockés par Firefox.

## Observations initiales
On a un gros paquet ch20.tgz qui contient le dossier navigateur  Firefox d’une personne, dans ce genre de dossier Firefox garde les mot de passe. 


La premiere chose que j’ai fait, c est regardé ce qu’il y a dedans: 

<img width="657" height="540" alt="image" src="https://github.com/user-attachments/assets/05da26f7-c580-4a36-a976-a521788a3864" />

C’est ce dossier la qui va nous intéresser

On va ensuite venir copier tout ces fichier pour les mettres dans un dossier propre 

Après ça, on voit un dossier .mozilla/firefox/o0s0xxhl.default c’est le profil Firefox. 

On sait que c’est du firefox 14 par le titre du chall, et quand on se renseigne on apprend 
que : Firefox 14  stocke les identifiants dans un fichier SQLite, et les clés/chiffrement 
dans key3.db.

Si l’utilisateur n’a pas défini de master password, il est possible de 
récupérer les mots de passe en clair assez facilement ;sinon il faut 
connaître/bruteforcer le master password. 

On va donc prendre ces 2 fichiers: 

<img width="560" height="61" alt="image" src="https://github.com/user-attachments/assets/4e3a293a-16dc-4295-86f7-c8bced086365" />

Puis installer un outil qui s’appele firefox_decrypt

<img width="657" height="75" alt="image" src="https://github.com/user-attachments/assets/ea3a3a2d-ada4-4f8b-9be3-b28aa471e7f3" />

Puis on execute: 

## Resultat

<img width="659" height="78" alt="image" src="https://github.com/user-attachments/assets/3da78913-c875-4c97-a1c5-3f7f31ccd808" />








