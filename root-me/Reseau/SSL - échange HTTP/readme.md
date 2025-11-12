## Contexte

Ce challenge est issu des épreuves de qualifications pour le CTF de la DEFCON.

INDICE : "google is your friend : inurl:server.pem..."

On à également une capture reseau pcap, qui nous ai fournis, contenant une session TLS entre 2 machines

Dans la capture on a handshake TLS puis paquets application_data (le HTTP chiffré).

Notre but donc c est de lire le HTTP en déchiffrant la session TLS

## Concept important 

### Reseau

TCP : protocole de transport qui crée une connexion fiable entre client et serveur

HTTP : protocole applicatif pour requêtes/réponses

TLS (HTTPS) : couche de chiffrement entre TCP et HTTP. On négocie d’abord TLS (handshake) puis on envoie le HTTP chiffré dans les paquets application_data

### Chiffrement

Chiffrement symétrique (ex. AES-256-CBC) : même clé pour chiffrer et déchiffrer, utilisé pour le flux de données (HTTP).

Chiffrement asymétrique (ex. RSA) : paire de clés publique/privée, utilisé pour échanger ou authentifier la clé symétrique.

### Certificat X.509

Contient la clé publique du serveur + des informations d’identité (CN, organisation), signé par une CA

Le certificat ne contient normalement pas la clé privée ; quand on trouve un .pem avec la clé privée, c’est généralement fuite ou un fichier de démonstration.


## Inspecter la capture

<img width="678" height="182" alt="image" src="https://github.com/user-attachments/assets/21c90068-6a10-45d9-9df7-89446ff5d705" />


On a bien du TLS_RSA donc on va pouvoir déchiffrer si on trouve la clé privée

Ensuite on va exporter le certificat

<img width="992" height="164" alt="image" src="https://github.com/user-attachments/assets/09dd5458-543d-490d-baba-659e6d4b1835" />

## Trouver le server.pem sur internet

On a l'indice l’indice inurl:server.pem

On trouve le server.pem 


