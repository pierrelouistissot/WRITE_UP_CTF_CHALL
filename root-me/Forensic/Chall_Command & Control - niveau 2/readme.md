## Contexte
Énoncé
Berthier, grâce à vous la machine a été identifiée, vous avez demandé un dump de la mémoire vive de la machine et vous aimeriez bien jeter un coup d’œil aux logs de l’antivirus. Malheureusement, vous n’avez pas pensé à noter le nom de cette machine. Heureusement ce n’est pas un problème, vous disposez du dump de memoire.

Le mot de passe de validation est le nom de la machine.

Le hash md5 du dump mémoire décompressé est e3a902d4d44e0f7bd9cb29865e0a15de


## Rappel

Un fichier dmp c est quoi?

C est une photo de la RAM (la mémoire vive) d’un ordinateur au moment où la machine était compromise.

### Ram

La RAM, c’est l’endroit où le PC met tout ce qu’il est en train d’utiliser :

programme,fichier,parametre systeme,conversation reseau,reglages internes

C est le bordel

Nous on veut retrouver le nom du pc:

Windows stocke ses réglages dans une base de données interne appelée :

**le registre**

Ce registre est découpé en hives
On y retrouve: SYSTEM,SOFTWARE,SECURITY,SAM,DEFAULT


**Donc** pour retrouver le nom de la machine on doit lire la bonne hives en l'occurence : SYSTEM


L'outil qu'on va utiliser c est VOLATILITY 3:

Qui permet d'analyser les fichiers dmp, il analyse le bordel et qui retrouve les fichiers qui nous interesse


## Resolution

Cette commande nous sort la liste des hives:

<img width="925" height="63" alt="image" src="https://github.com/user-attachments/assets/7e276281-851f-47b2-b76a-11ec63acc4fc" />

On obtient :

<img width="888" height="290" alt="image" src="https://github.com/user-attachments/assets/7963834a-b21d-4da8-b421-f5183dad7d52" />

On à donc l'adresse de SYSTEM

**0x8b21c008**
Maintenant qu’on sait où est SYSTEM, on peut ouvrir la bonne clef :

<img width="1094" height="229" alt="image" src="https://github.com/user-attachments/assets/572aacce-7b78-4d69-b650-6426aed93db7" />

FACILE!!!!!!










