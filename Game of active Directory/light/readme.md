On commence avec un scan nmap:




<img width="1331" height="869" alt="image" src="https://github.com/user-attachments/assets/e6267605-9706-45c8-be43-cf16f501fadd" />

192.168.56.10 — KINGSLANDING → ports 53, 88, 389 ouverts = Domain Controller confirmé du domaine sevenkingdoms.local. RDP accessible aussi.
192.168.56.11 — WINTERFELL → même profil = Domain Controller confirmé, même domaine visible mais c'est en réalité north.sevenkingdoms.local (le child domain).
192.168.56.22 — nom inconnu → pas de DNS, pas de Kerberos, pas de LDAP = ce n'est pas un DC, c'est SRV02 (castelblack). Par contre SMB (445) et RDP sont ouverts — c'est un serveur membre intéressant à attaquer.


La première chose qu'on fait toujours c'est tenter une connexion anonyme sur SMB beaucoup d'environnements AD laissent traîner des infos accessibles sans mot de passe :

<img width="2022" height="174" alt="image" src="https://github.com/user-attachments/assets/456ad3de-a633-4705-937d-133cf8912d83" />


On voie que :
Sur les 2 DCs, on peut se connecter en SMB sans mdp, c est une misconfiguration classique, qui va nous permettre d'enumerer anonymement des infos sur le domaine
Et sur le serveur on a signing false, donc meme pas besoin que les paquets smb soit signé cryptographiquement, donc on pourrait penser a fair edu ntlm replay typiquement
