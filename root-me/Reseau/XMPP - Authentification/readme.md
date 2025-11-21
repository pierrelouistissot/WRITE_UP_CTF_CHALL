## Contexte

En espionnant par dessus l’épaule de l’utilisateur au moment où il s’authentifiait, il semblerait que son mot de passe contienne une partie du login. Retrouvez le mot de passe de l’utilisateur dans cette capture réseau de session XMPP.
Le flag est le condensat SHA1 de ce mot de passe.

## XMPP, c’est quoi ?

XMPP = Extensible Messaging and Presence Protocol
C’est un protocole de messagerie instantanée:
discutter en temps réel,envoyer des status,ect... C est base sur du xml qui transite grace a du tcp
Facebook Chat (avant 2015), Jabber (le réseau originel XMPP)

On dois se connecter au serveur XMPP, il nous faut un mdp de login
Comme pour un serveur mail, mais ici c'est pour un service de messagerie.

Authentification la plus courante aujourd’hui pour XMPP est: SASL SCRAM (Salted Challenge Response Authentication Mechanism)


##   SCRAM-SHA1 : comment ça marche ?


Ce que SCRAM garantit:

Le mot de passe n’est jamais envoyé sur le réseau.
Le serveur et le client s’envoient des preuves cryptographiques.

| Le client envoie    | Le serveur repond |
|--------------- |------------------|
| client nonce        | son server nonce |
| son username        | un salt |
| Scram encodées en BS64   | un iteration count |




Puis le client envoie :

une client proof = dérivée cryptographique du mot de passe

Donc l’attaque classique consiste à :

Test de mots de passe (brute force / dictionnaire) sur la client proof + sel + itérations.




## Analyse

### Client → Serveur : client-first-message

<img width="723" height="209" alt="image" src="https://github.com/user-attachments/assets/3bf53d20-5fd2-4bc8-9da2-cad2a657ce94" />


Je decode cette valeur en base64, j'obtiens:n,,n=koma_test,r=hydra

A partir de ce Cdata on obtient le username=koma_test et le nonce client=hydra

### Serveur → Client : server-first-message

<img width="845" height="130" alt="image" src="https://github.com/user-attachments/assets/85992910-3228-4633-b888-8af3cb0254ad" />

Apres la bs64 on a :

```
r=hydraFe3A1scL7C0jtKsm+kcg96MWg769FuRu,s=kM6lTjjnZW4F8WLboyagcA==,i=4096

```
r= : nonce complet = client nonce + partie serveur
→ commence par hydra... → le serveur ajoute sa partie.

s= : salt (sel), encodé en base64

i= : nombre d’itérations PBKDF2 → 4096



### Client → Serveur : client-final-message

<img width="909" height="139" alt="image" src="https://github.com/user-attachments/assets/030015d2-d3a1-4b99-a664-47a7edca9e03" />

c= : channel binding, ici biws = base64 de n, (détail protocole).

r= : même nonce complet que côté serveur.

p= : ClientProof (preuve du client) → c’est ce qui remplace “envoyer le mot de passe”.


### Serveur => Client : final message

<img width="492" height="126" alt="image" src="https://github.com/user-attachments/assets/5843ae3e-155b-41e4-b17e-bd63e0a1a2c7" />

```
v=YQlegvbEwDo2o60YiK2iAkYyPKE=

```
v= : ServerSignature, une preuve que le serveur connaissait aussi le bon secret dérivé du mot de passe.

```
initial_message = "n=koma_test,r=hydra"
server_first_message = "r=hydraFe3A1scL7C0jtKsm+kcg96MWg769FuRu,s=kM6lTjjnZW4F8WLboyagcA==,i=4096"
server_final_message_compare = "v=YQlegvbEwDo2o60YiK2iAkYyPKE="  valeur qu'on veut retrouver

```

L’idée de l’attaque :

Tu choisis un password candidat, tu rejoues tout l’algorithme SCRAM côté client, tu recalcules v=… et tu compares au v vu dans la capture.
Si ça matche ⇒ tu as trouvé le vrai mot de passe.

Pour chaque candidat, le script :

dérive le mot de passe avec PBKDF2

calcule les HMAC (ClientKey, ServerKey)

construit le authMessage

calcule la signature serveur v= comme le vrai serveur




## Resultat

<img width="453" height="87" alt="image" src="https://github.com/user-attachments/assets/d5703097-77a8-47e6-a9ed-221a3b93e404" />

