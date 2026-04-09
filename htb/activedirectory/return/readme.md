
<img width="1252" height="583" alt="image" src="https://github.com/user-attachments/assets/9257990b-00f0-4416-9f61-29df65914496" />

<img width="1252" height="583" alt="image" src="https://github.com/user-attachments/assets/b3f0d831-e69c-4d86-b135-9e883240a542" />

On voit :

Le site c'est le site de l'imprimante, et dans setting on a les creds de l'imprimante pour se connecter a l'ad via ldap

```
Site web (port 80)
└── c'est l'interface d'admin de l'imprimante

Settings du site
└── Server Address : printer.return.local  → où est l'AD
└── Port : 389                             → port LDAP
└── Username : svc-printer                 → compte de service AD
└── Password : *******                     → mot de passe de ce compte

```
<img width="939" height="538" alt="image" src="https://github.com/user-attachments/assets/17e70ae1-7148-49ee-992c-79cd12557f26" />

le svc-printer est server-operators


