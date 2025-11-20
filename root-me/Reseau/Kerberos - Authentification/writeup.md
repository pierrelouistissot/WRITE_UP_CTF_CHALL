## Contexte

Énoncé
Vous êtes mandaté par l’équipe SOC de l’entreprise Cat Corporation pour retrouver le mot de passe d’un utilisateur lié à une connexion Kerberos suspecte.

Format du flag : RM{userPrincipalName:password}

L’userPrincipalName doit être écrit en minuscules.


On a une trame reseau, on va se consacrer sur le protocol KRB5

<img width="1696" height="892" alt="image" src="https://github.com/user-attachments/assets/1448c213-8415-42a5-9091-00c9562ae527" />


## Fonctionnement général de kerberos

Kerberos est le mécanisme principal d’authentification utilisé dans Active Directory.

1. Client

Machine ou utilisateur qui veut s’authentifier.

2. KDC (Key Distribution Center)

Serveur AD contenant la base des utilisateurs et l’ensemble des clés de sécurité.

3. Services (serveurs, partages SMB, etc.)

Les services font confiance aux tickets délivrés par le KDC.

### Etape clef

AS-REQ (sans pré-auth)
Le client commence par envoyer une requête au KDC :
Mais le KDC refuse et répond :

<img width="1065" height="26" alt="image" src="https://github.com/user-attachments/assets/4942cc1b-9fd1-4e3e-9715-3e69ceb01917" />

Parce qu’Active Directory impose une protection appelée "PreAuthentication" afin d’éviter les attaques par rejeu (replay attacks).

### La pré-authentication Kerberos

Le client doit prouver qu’il connaît son mot de passe... sans l’envoyer en clair.

Pour cela, il envoie :

un timestamp chiffré

Ce timestamp est chiffré avec une clé dérivée du mot de passe de l’utilisateur.

C’est ce champ que nous avons dans ta capture.

<img width="781" height="69" alt="image" src="https://github.com/user-attachments/assets/2e588f95-3c17-4a87-a2fb-c49a65fd6879" />

Le KDC ne nous fournit aucune information, mais par contre le client lui envoie un message chiffré  qui depend de son mot de passe :

** Donc si on capture ce message, on peut tenter de le déchiffrer hors-ligne. **

C’est ce qu’on appelle l’attaque AS-REQ Roasting.

Il s’agit de l’équivalent de Kerberoasting, mais pour la phase PreAuth.



### Analyse

Dans la trame, photo ci_dessus on voit etype: eTYPE-AES256-CTS-HMAC-SHA1-96 (18) et c 'est parfait puis c est ducoup crackable via Hashcat en mode 19900

Donc on recupere le champs 

Cipher: fc8bbe22b2c967b222ed73dd7616ea71b2ae0c1b0c3688bfff7fecffdebd4054471350cb6e36d3b55ba3420be6c0210b2d978d3f51d1eb4f

On construit le hash Format Hashcat pour Kerberos PA-ENC-TIMESTAMP (etype 18) :
`
$krb5pa$18$<username>$<realm>$<cipher>

`

Donc on obtient:

`
$krb5pa$18$william.dupond$CATCORP.LOCAL$fc8bbe22b2c967b222ed73dd7616ea71b2ae0c1b0c3688bfff7fecffdebd4054471350cb6e36d3b55ba3420be6c0210b2d978d3f51d1eb4f


`

Puis on crack : hashcat -m 19900 -a 0 hash.txt /usr/share/wordlists/rockyou.txt






