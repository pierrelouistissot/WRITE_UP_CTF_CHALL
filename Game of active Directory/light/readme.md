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

<img width="2030" height="406" alt="image" src="https://github.com/user-attachments/assets/b3d2a777-c302-4293-9a3a-10a153e6e09e" />

On voit que le compte est valide
Ensuite on se fait passer pour samwell.tarly, et on cherche tout les compte qui font tourner un service(spn) et on genere un ticket pour chacun



<img width="2030" height="935" alt="image" src="https://github.com/user-attachments/assets/f2cfaf77-9eba-4d8d-840a-ad7c11e4ae4c" />

On va essayer de trouver les mdps avec hashcat:

Avec la wordlist crackstation et la rule: best64 on trouve 2 hash:

<img width="2030" height="558" alt="image" src="https://github.com/user-attachments/assets/4b1908ab-f076-414b-af45-5204f71d78d7" />

On va donc essyaer de se connecter a leur compte:

D'abord John snow:

netexec smb 192.168.56.0/24 -u 'jon.snow' -p 'iknownothing' 


<img width="2030" height="230" alt="image" src="https://github.com/user-attachments/assets/7454fdd6-980c-4fa6-a087-781c6f07604a" />

KINGSLANDING refuse, c'est normal, jon.snow appartient à north.sevenkingdoms.local, pas à sevenkingdoms.local. Les deux domaines sont distincts et ne partagent pas automatiquement leurs comptes.
CASTELBLACK accepte, CASTELBLACK est un serveur membre de north.sevenkingdoms.local, donc il reconnaît jon.snow.
Mais il n'y a pas (Pwn3d!) sur CASTELBLACK. Ça veut dire que jon.snow peut s'authentifier mais il n'est pas administrateur local sur cette machine.

On va donc voir a quoi a acces jon.snow sur CASTELBACK

<img width="2030" height="230" alt="image" src="https://github.com/user-attachments/assets/7456f93b-6413-45f2-9909-7e9cf49b937b" />


<img width="2030" height="808" alt="image" src="https://github.com/user-attachments/assets/275c0b2f-82ab-41d3-90d1-c6a8a0e7b124" />

A premiere vue rien d'interessant, le seul truc suspect c est qu'on puisse ecrire dans le share, et c est pareil pour le 2 ieme utilisateur trouve, elle exactement les meme droits


Je suis un peu perdu, je vais utiliser bloodhound

<img width="1794" height="92" alt="image" src="https://github.com/user-attachments/assets/571ffec6-b171-4cd5-a743-1d9fd0f01c24" />


SAMWELL.TARLY
    │
    ├── WriteDacl  ──▶  STARKWALLPAPER (GPO)
    └── WriteOwner ──▶  STARKWALLPAPER (GPO)
                              │
                              ▼
                        NORTH.SEVENKINGDOMS.LOCAL (domaine)
                              │
                              ▼
                        USERS@NORTH.SEVENKINGDOMS.LOCAL
                              │
                              ▼
                        DOMAIN ADMINS@NORTH.SEVENKINGDOMS.LOCAL


Normalement seuls les Domain Admins peuvent modifier les GPOs.
Mais samwell.tarly a WriteDacl sur STARKWALLPAPER — ça veut dire qu'il peut modifier les permissions de cette GPO pour se donner le droit de l'éditer.
Et WriteOwner — il peut se définir comme propriétaire de la GPO, ce qui lui donne automatiquement tous les droits dessus.

<img width="1085" height="142" alt="image" src="https://github.com/user-attachments/assets/28b7adde-92f7-464c-9849-c4a048c90f17" />

<img width="1675" height="161" alt="image" src="https://github.com/user-attachments/assets/a8ade9d7-cd63-4d82-b9ed-095314387c8d" />

<img width="1681" height="108" alt="image" src="https://github.com/user-attachments/assets/5c831448-099b-4109-a0ec-780c0e255b1d" />

1. Scan réseau (nmap)
   → Découverte de 3 machines

2. Enumération SMB anonyme (netexec)
   → Trouvé samwell.tarly avec son mdp en clair

3. Kerberoasting
   → Récupéré les hashes de jon.snow, sansa.stark, sql_svc
   → Cracké jon.snow:iknownothing et sansa.stark:345ertdfg

4. BloodHound
   → Découvert que samwell.tarly a WriteDacl/WriteOwner
     sur la GPO StarkWallpaper

5. GPO Abuse (pygpoabuse)
   → Injecté une tâche planifiée dans la GPO
   → Créé un compte admin local "hacker" sur CASTELBLACK

6. Résultat : admin local sur CASTELBLACK




On peut maintenant tester de dumper les hashes NTLM locaux ou les secrets LSA


<img width="1684" height="670" alt="image" src="https://github.com/user-attachments/assets/1882be69-c845-491e-b174-8280f18430f6" />

Administrator  => hash: dbd13e1c4e338284ac4e9874f7de6ef4
vagrant        => hash: e02bc503339d51f71d913c245d35b50b
hacker         => hash: 2b576acbe6bcfda7294d6bd18041b8fe

sql_svc   => YouWillNotKerboroast1ngMeeeeee 
robb.stark => hash DCC2 (cracable)

<img width="1684" height="283" alt="image" src="https://github.com/user-attachments/assets/fe97c62d-6b14-4870-ab82-c77c86fb45a5" />











