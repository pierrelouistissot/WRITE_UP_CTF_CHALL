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

On trouve le server.pem ==> [server.pem](./server.pem)

Avant de trouver la bonne, j'en ai testé pas mal, ducoup pour voir si c'etais la bonne je comparer les modudulus:


<img width="897" height="113" alt="image" src="https://github.com/user-attachments/assets/fd5263c2-838c-411c-a1c8-d63fa773794d" />


Si les trois valeurs MD5 sont identiques, alors on est bon

### Resultat

Une fois la bonne clé trouvé, on va dans wireshark

Edit => Preferences => Protocols => TLS => RSA keys list => New =>

<img width="961" height="794" alt="image" src="https://github.com/user-attachments/assets/97274772-f8b8-4282-8cad-265b134eca83" />

Puis on va dans  Analyze=>Follow=>TLS Stream => et BAM le flag apparait, vous avez reussi a dechiffrer le HTTP en clair!

### PTS IMPORTANT

Tu ne peux pas extraire une clé privée d’un pcap.


Tu peux extraire le certificat depuis le pcap.


Si la session a utilisé RSA key exchange, et si tu trouves la clé privée correspondante  alors tu peux reconstruire la clé symétrique (AES) et décrypter le HTTP.





