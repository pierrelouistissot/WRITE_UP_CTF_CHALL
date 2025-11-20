## Contexte

SNMP – Authentification (SNMPv3)
Récupérer le mot de passe qui a été utilisé pour authentifier l’échange SNMP de la capture réseau.

On nous donne un fichier .pcap contenant quelques paquets réseau. L’idée est de récupérer le mot de passe SNMPv3 utilisé pour l’authentification.


## Protocole

SNMP (Simple Network Management Protocol) sert à manager des équipements réseau (routeurs, switches, etc.) :

Un manager (mon PC) envoie des requêtes (GET, SET…) à un agent (équipement).
L’agent répond avec les infos (CPU, interfaces, etc.).

<img width="850" height="230" alt="image" src="https://github.com/user-attachments/assets/0602b768-a187-4214-b249-8ab1d789b060" />

EngineID : identifiant unique de l’agent SNMP (la machine surveillée).

UserName : le compte SNMPv3 utilisé → ici "user".

msgAuthenticationParameters : c’est là qu’est stocké le HMAC-MD5-96, donc la “signature” du message.

msgPrivacyParameters : <MISSING> → il n’y a pas de chiffrement, seulement de l’authentification (on est en mode authNoPriv).

Donc : le message n’est pas chiffré, mais il est signé avec un HMAC. Ça veut dire :

** On peut lire tout ce qu’il y a dedans, mais on ne peut pas le modifier sans connaître le mot de passe.**

## SNMPv3 en mode Authentification

Pour chaque utilisateur , on peut configurer:

Un authProtocol : Dans notre cas MD5
un authPassword : Celui qu'on veut retrouver

Ce qui nous intéresse :

Pour authentifier un message, SNMPv3 calcule un HMAC-MD5-96 sur le message, en utilisant un authKey dérivé du mot de passe.


### HMAC-MD5-96

#### MD5

MD5 = fonction de hash.
Tu lui donnes des données, elle renvoie une empreinte de 128 bits (16 octets).

#### HMAC
HMAC = Hash-based Message Authentication Code.

On veut une “signature courte” du message, qui prouve que quelqu’un qui connaît la clé l’a calculée, et que le message n’a pas été modifié.

DONC: le ``` HMAC-MD5```
```
HMAC(key, message) = MD5( (key ⊕ opad) || MD5( (key ⊕ ipad) || message ) )
```
ipad = 0x36 répété

opad = 0x5c répété

⊕ = XOR

|| = concaténation

MAIS en gros: On mélange clé et message via MD5 de façon spéciale → HMAC.
Resultat : on obtient un hash de 128 bits, comme un md5 classique

ET le 96?

Bah on garde juste les 96 premiers bits du hash ==> 12 octets

### Comment on a la clef?

le mot de passe que nous on veut retrouver n'est pas utilisé directement au moment du hmac-md5, on le tranforme en Ku( clé de 16 octets)

#### Creation du Ku

On concatène le mot de passe sur 1 Mo de données (1 048 576 octets), en le répétant
On fait MD5 sur ce giga tas de caractères → ça donne Ku, 16 octets.

#### Kul => Clé localisé
SNMP utilise le principe de clé localisée par appareil:

On prend l'engine ID du device
On calcul: Kul = MD5( Ku || EngineID || Ku )

Peu importe où on configures le même mot de passe, la clé Kul sera différente sur chaque agent, car l’EngineID change

#### Kul => Clé HMAC

À partir de Kul, on dérive la clé HMAC
On l’étend à 64 octets (en ajoutant des 0x00 à la fin).
On XOR avec ipad et opad pour faire k1 et k2.
On calcule le HMAC comme vu au-dessus, sur le message SNMP entier, avec un détail important :
Pour calculer l’HMAC, le champ msgAuthenticationParameters doit être rempli de zéros.

## l’algorithme réel


Prendre le message SNMP complet, mais avec le champ digest remplacé par 00 00 00 00 00 00 00 00 00 00 00 00.
Calculer HMAC-MD5(Kul, message_modifié).
Tronquer le résultat à 12 octets → c’est msgAuthenticationParameters.


Et côté réception :

Le serveur refait la même chose avec sa copie de la clé,
Compare les 12 octets calculés avec ceux du paquet,
Si ça match → mot de passe correct et message intact.



## Comment on attaque çe bordel

On a: 
```
Le message complet (en hex) → msg.

Le digest HMAC-MD5-96 → target = "b92621f4a93d1bf9738cd5bd".

L’EngineID → "80001f8880e9bd0c1d12667a5100000000".

Le username → user.

L’info que c’est de l’authMD5 (MD5 comme algorithme d’authentification).

Un dictionnaire de mots de passe (fichier RootMe).

```

### Comment on fait

On va donc faire un code qui vient brutforce la clé


Il prépare les infos fixes de la trame SNMPv3

MSG_HEX : la trame SNMPv3 complète (frame 3) en hex.

AUTH_HEX : la valeur d’auth qu’on voit dans Wireshark (le digest qu’on veut retrouver).

ENGINEID_HEX : l’EngineID de l’agent SNMP.
Ça, c’est le « contexte » de l’échange, qui ne bouge pas.



Il sait calculer le digest SNMPv3-MD5 pour un mot de passe donné (compute_snmpv3_md5)
Pour un password :

Il génère la clé Ku à partir du mot de passe (MD5 sur 1 Mo de répétitions du mot de passe).

Il la « localise » avec l’EngineID pour obtenir Kul.

Il remplace le champ d’authentification dans la trame par des zéros (msg_zeroed) et fait un HMAC-MD5 avec Kul sur ce message-là.

Il garde seulement les 12 premiers octets (HMAC-MD5-96) et les renvoie en hex.

Il brute-force avec un dictionnaire (brute_force)


Pour chaque mot :

il calcule le digest SNMPv3 avec compute_snmpv3_md5(password)

il compare au digest de la capture (AUTH_HEX).

Si ça matche → il affiche : Mot de passe trouvé






























<img width="277" height="151" alt="image" src="https://github.com/user-attachments/assets/30c39b3c-c16b-4ac7-bd8b-fe3c6ef20a1a" />

