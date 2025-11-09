## Contexte
Objectif : récupérer le contenu d’une archive ZIP protégée par mot de passe fournie par le challenge Root-Me.
## Analyse initiale
J'ai commencé par inspecter l’archive pour connaître son format et la méthode de compression.

<img width="939" height="68" alt="image" src="https://github.com/user-attachments/assets/b07f0711-e2a1-4ad1-91a7-d78cd9a945ad" />

Interprétation : archive ZIP standard (méthode deflate). Cela permet d’utiliser des 
attaques par dictionnaire classiques (ZipCrypto / PKZIP compatible). 
J’ai donc utiliser un dictionnaire classique:Rockyou 

<img width="657" height="112" alt="image" src="https://github.com/user-attachments/assets/5e194a7b-d5e8-4bc8-b81c-2c98fa840984" />


On trouve bien le password

## Résultat

Avec ce mot de passe, l’archive s’extrait correctement et permet d’accéder aux fichiers fournis par le challenge.
