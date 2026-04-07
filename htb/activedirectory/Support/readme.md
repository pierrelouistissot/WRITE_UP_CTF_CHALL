### Enumeration


<img width="1324" height="343" alt="image" src="https://github.com/user-attachments/assets/3659e4a6-f73d-4abf-b702-d8bf7cfe3877" />


<img width="628" height="262" alt="image" src="https://github.com/user-attachments/assets/5bd011e3-a9f1-49d8-9e9a-e03aa01e5c93" />



### Trouvaille

On voit qu'on a plusieurs share accesible:
<img width="1324" height="790" alt="image" src="https://github.com/user-attachments/assets/66f410a6-ffb0-4caf-9fb2-1515226c585a" />

On va essayer de "reverse" le fichier UserInfo.exe, 

<img width="1324" height="687" alt="image" src="https://github.com/user-attachments/assets/e27dfe59-2fe5-4c90-b442-717db2565a58" />

monodis nous a donné l'algorithme exact
ldstr "0Nv32PTwgYjzg9/8j5TbmvPd3e7WhtWWyuPsyO76/Y+U193E"

FromBase64String(enc_password)   => décode le base64

XOR avec key[i % key.length]     =>  XOR avec "armando"

et ldc.i4 0xDF, une constante supplémentaire XORée

<img width="1324" height="221" alt="image" src="https://github.com/user-attachments/assets/2d8e3e5b-4faa-4d1d-99f8-80c0247a8092" />


On trouve ce mdp:`nvEfEK16^1aM4$e7AclUf8x$tRWxPWO1%lmz`

Maintenant on dump le ldap:

<img width="1324" height="454" alt="image" src="https://github.com/user-attachments/assets/8d8d9299-4131-4905-a01d-d986ccd0bf15" />

Dans le dump ldap on trouve ca:

<img width="542" height="107" alt="image" src="https://github.com/user-attachments/assets/a2b3ea6a-6f7a-4530-8930-1b5a5fe22bd5" />

On peut donc se connecter en WinRM

<img width="658" height="348" alt="image" src="https://github.com/user-attachments/assets/5b9aa2f9-888f-470a-b2c8-1eea292f7a18" />


Maintenant qu'on a acces au compte support, on va regarder ces droits et voir si on peut pas monter en privilieges



On utilise bloodhound:

<img width="1702" height="178" alt="image" src="https://github.com/user-attachments/assets/c545d9c3-ae81-40e6-862d-e81c51c4d1a0" />


Support est membre de Shared Support Accounts ==> Ce groupe a GenericAll sur le DC ==> GenericAll = contrôle total sur l'objet ==> on peut faire ce qu'on veut sur le DC


On peut donc faire une: Resource Based Constrained Delegation

On va utiliser Impacket:

Impacket c'est une collection de scripts Python qui réimplémentent des protocoles réseau Windows , permet d'interargir avec des service windows depuis linux

Voila la pipeline que je vais utiliser:

```
1. addcomputer.py  ==> crée FAKE$ dans l'AD
2. rbcd.py        ==> dit au DC "FAKE$ peut agir au nom de n'importe qui"
3. getST.py        ==> demande un ticket en se faisant passer pour Administrator
4. psexec.py       ==> utilise ce ticket pour se connecter en SYSTEM

```

<img width="728" height="178" alt="image" src="https://github.com/user-attachments/assets/583de600-03e8-44e0-b575-fa0d77327d46" />

<img width="728" height="261" alt="image" src="https://github.com/user-attachments/assets/a1407476-cf0b-43c1-af20-2928e6525e3e" />

<img width="746" height="261" alt="image" src="https://github.com/user-attachments/assets/fd7692ee-9323-4c7b-9bc8-ae0b44d0b3e7" />

<img width="746" height="355" alt="image" src="https://github.com/user-attachments/assets/eba091fa-3b19-44a3-9666-c88584879210" />






