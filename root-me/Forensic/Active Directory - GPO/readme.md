## Contexte 

Une capture réseau réalisée au démarrage d’une station de travail, membre d’un domaine Active Directory, a été effectuée lors d’un audit de sécurité. Analysez cette capture et retrouvez le mot de passe de l’administrateur.


Lors d’un audit de sécurité dans une entreprise, un technicien a enregistré le trafic réseau généré par le démarrage d’un poste Windows appartenant au domaine Active Directory de l’entreprise.
Active Directory, c’est le système utilisé dans beaucoup d’entreprises pour gérer :

les comptes utilisateurs,les PC de l’entreprise et les règles qui s’appliquent automatiquement aux machines.

Au démarrage, chaque PC du domaine se connecte au serveur Active Directory pour récupérer ces règles, qu’on appelle GPO (Group Policy Objects).
Certaines de ces règles utilisent un mécanisme appelé Group Policy Preferences (GPP), qui permet d’automatiser des actions comme : créer un utilisateur, configurer un service, installer une imprimante… et parfois définir un mot de passe.

On sait que windows utilise SBM/SBM2 pour partager des fichiers sur le réseau

le partage SYSVOL

accessible en SMB / SMB2 : \\domaine.local\SYSVOL\...

## Analyse

Lorsque un PC démarre et rejoint le domaine, voici ce qu’il fait :

Il contacte le serveur AD.

Il télécharge les GPO nécessaires.

Et il récupère les fichiers XML GPP via SMB dans SYSVOL.

Donc dans la capture réseau, il faut chequer des échanges SMB/SMB2 où le PC télécharge un fichier XML depuis SYSVOL.

<img width="1877" height="777" alt="image" src="https://github.com/user-attachments/assets/dccb2598-3499-427d-ace6-d314285436f1" />



Ensuite on click dessus et on fait follow tcp stream



<img width="1230" height="94" alt="image" src="https://github.com/user-attachments/assets/7040729a-cd9e-4648-9320-b848644f6025" />



On chope le mdp, mais on doit maintenant le dechiffrer:

Pour déchiffrer le champ cpassword, j’utilise un outil public “gpp-decrypt” qui implémente l’algorithme connu pour les Group Policy Preferences (AES-256 avec la clé documentée par Microsoft).

En lui passant la valeur cpassword trouvées :

LjFWQMzS3GWDeav7+0Q0oSoOM43VwD30YZDVaItj8e0

j’obtiens les mots de passe en clair.


<img width="744" height="42" alt="image" src="https://github.com/user-attachments/assets/c378ee6a-9065-48fe-99c0-2add3763cf25" />














