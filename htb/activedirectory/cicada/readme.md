<img width="854" height="346" alt="image" src="https://github.com/user-attachments/assets/72111b03-831a-458e-a21b-f4ad38e3a37b" />

On voit que le port smb est ouvert:

SMB: protocole utilisé par Windows pour partager les dossiers/fichiers/administration a distance

on fait donc 

<img width="812" height="256" alt="image" src="https://github.com/user-attachments/assets/baa7b5de-a967-4070-b5f2-030e3944620e" />

Ca veut dire en gros : Montre-moi tous les dossiers partagés accessibles sans mot de passe.


On peut donc voir les différents dossiers partagés, maintenant on aimerait voir ce qu'il y a dedans:

On va donc tenter des les ouvrirs, un par un, sauf ce qui ont des $ car il faut etre admin:

<img width="816" height="244" alt="image" src="https://github.com/user-attachments/assets/3efa5063-432c-4a6a-a94b-9f32efdd4a1d" />

Dev n'a pas fonctionné, mais par contre HR a fonctionné:

On y trouve un fichier txt, on va donc le télécharger en faisant un `get`, puis l'ouvrir, on obtient ca:


<img width="1871" height="470" alt="image" src="https://github.com/user-attachments/assets/18bdcb20-1ab0-421d-80ee-60c8109e314c" />


`Your default password is: Cicada$M6Corpb*@Lp#nZp!8
`

On a un mot de passe, il faudrait maintenant trouver un compte qui a garder le mdp standard:
Pour cela, on utilise RPC le port 135
On utilise lookupsid.py, pour bruteforce les SID, en gros on demande a qui correspond tel SID, pour ensuite avoir tout les utilisateurs.

<img width="1848" height="747" alt="image" src="https://github.com/user-attachments/assets/89764a3c-d797-41c6-b1b7-f43b84b203ff" />

On voit qu'on trouve plein de user a la fin donc on met tout ces users dans un fichiers et on viens tester un par une connexion smb avec le mot de passe trouvé:

<img width="1956" height="391" alt="image" src="https://github.com/user-attachments/assets/6ea85976-f13b-4e24-8e32-5d226e448c7c" />

HOP on trouve un compte qui a bien ce mot de passe: `michael.wrightson`

On reessaye de connecter et d'aller chequer les shares dans le smb , mais on a toujours pas les acces, par contre on a les acces pour voir les differents user presents, 

On va donc interroger AD avec son protocol ldap:


<img width="1956" height="138" alt="image" src="https://github.com/user-attachments/assets/122bb9de-2ee4-44bd-badd-1f208190ebf2" />

<img width="1956" height="80" alt="image" src="https://github.com/user-attachments/assets/1e9d1650-5b7a-4f70-968b-7ac032b1021e" />

On a donc un deuxieme compte, on va voir si il a acces au share:












