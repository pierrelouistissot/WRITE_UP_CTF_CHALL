
## Contexte

Après lancement du challenge, on se connecte en SSH sur la machine fournie :
```
ssh -p 22222 root@ctf05.root-me.org

```

Le système est une Ubuntu minimaliste, réduite au strict nécessaire.
On doit donc nous-mêmes installer certains outils pour analyser le réseau.

L'objectif global du challenge est de réaliser une attaque ARP Spoofing pour se placer en Man-In-The-Middle et intercepter une requête contenant des informations sensibles.

## Comprendre l'environnement

<img width="700" height="315" alt="image" src="https://github.com/user-attachments/assets/12926337-be7a-4a9d-8bd3-c1d3308563fe" />

#### Interpretation

ifconfig, nous montre 2 interfaces:

l’interface eth0

l’interface lo (loopback==> le, receveur et l'envoyeur sont les memes)

On comprend que :

Notre machine a l’adresse 172.18.0.2
Le masque 255.255.0.0 indique un réseau en /16
donc le LAN s’étend de 172.18.0.0 à 172.18.255.255 soit (16^2 appareils possibles)

**Avant un ARP Spoof, on doit connaître notre IP et notre interface, pour pouvoir sniffer le trafic ou lancer l’empoisonnement ARP sur la bonne interface.**

On verifie le cache ARP local

<img width="491" height="35" alt="image" src="https://github.com/user-attachments/assets/5edc37e2-977c-415f-996f-629b214d060d" />

#### Interpretation

Notre machine ne connaît qu’une seule autre adresse IP : 172.18.0.1
Cette IP est très probablement la gateway du réseau, car elle finit en .1 (adressage classique)

#### Rappel technique 

Le protocole ARP (Address Resolution Protocol) sert à faire la correspondance IP==> MAC 

Chaque machine garde les correspondance dans une table : le cache ARP

C’est précisément ce cache que l’on va manipuler avec ARP Spoofing, mais pour cela il faut deux cibles : la gateway et une victime.

**Pourquoi la victime n’apparaît pas encore**

Une machine n’apparaît dans le cache ARP que si on a communiqué avec elle.
Comme rien n’a encore communiqué avec notre VM :

le cache ARP est vide → sauf la gateway
on ne voit aucune victime
on doit donc scanner le réseau pour les découvrir

### Scan NMAP

On install nmap, en faisant "apt update" puis "apt install nmap -y"

On a vu que le reseau c etais du 172.18.0.0 donc on fait un "nmap -sn 172.18.0.0/16"


<img width="625" height="266" alt="image" src="https://github.com/user-attachments/assets/6054ffe3-802f-4cc2-baa7-8114cdecf480" />


On a 2 nouveau appareil decouvert sur le reseau le client en 4 et la db en 3
On a donc pour objectif de se placer entre les 2 machines pour intercepter leurs communications, c'est le principe d'un MITM

Je dois faire en sorte que tout le trafic entre 172.18.0.3 et 172.18.0.4 passe par ma machine

je fais croire au client que je suis la DB, je fais croire à la DB que je suis le client

Donc les 2 machines m'envoient leurs paquets, MAIS Si ma machine ne les retransmet pas ensuite à la vraie destination la connexion entre le client et la DB s’effondre complètement.

On va donc chequer si le paquets forwarding fonctionnent Avec la commande :
```
cat /proc/sys/net/ipv4/ip_forward
```
#### rappel

On va voir 0 ou 1 :

0 = forwarding désactivé  1 = forwarding activé

Pourquoi ce fichier existe ?

/proc représente des “pseudo-fichiers” qui montrent l’état interne du noyau Linux
ce fichier en particulier contrôle le comportement du réseau IPv4

la valeur dedans dit simplement :

“Est-ce que je me comporte comme un routeur, oui ou non ?”

<img width="541" height="38" alt="image" src="https://github.com/user-attachments/assets/f89d6560-b7a4-440d-83c7-70ce60395d5d" />

On a bien 1, le forwarding est activé, on peut continuer

### Analyse des machines

l’objectif de l’attaque MITM est de voler une requête entre le client et la base de données.

Donc on dois vérifier :

est-ce que le client parle à quelque chose ? si oui, sur quel port ? est-ce que c’est MySQL ?est-ce qu'on peut sniffer ce trafic ?



<img width="786" height="307" alt="image" src="https://github.com/user-attachments/assets/86b83ce0-2ad2-4636-820b-17f747d5ea01" />


On scanne d'abord le client avec la commande ``` nmap 172.18.0.4 ```, on nous dis que tout les ports sont fermées

On scanne ensuite la db, et on voit que le port 3306 est ouvert, ce port correspond au service mysql.

**Donc le client peut interroger cette bdd**



## On passe à l'attaque


<img width="942" height="151" alt="image" src="https://github.com/user-attachments/assets/d670bce9-cf00-437b-b60d-129e1451e15f" />

```
arpspoof -t 172.18.0.3 -r 172.18.0.4

```
-t 172.18.0.3 → la cible = la bdd
-r 172.18.0.4 → on lui ment en disant :
"l’IP 172.18.0.4 (le client ) a l’adresse MAC de ma machine"

Donc la bdd pense que je suis le client 

```
arpspoof -t 172.18.0.4 -r 172.18.0.3

```
-t 172.18.0.4 → la cible = le client
-r 172.18.0.3 → on lui ment en disant :
"l’IP 172.18.0.3 (la bdd) a l’adresse MAC de ma machine"

**Donc** le client envoie ses paquets vers ma machine et  la bdd renvoie ses réponses vers ma machine 

les `> /dev/null 2>&1` permettent de masquer toute la sortie de arpspoof, sinon le terminal est remplie de spma arp et le `&` signifie "lance la commande en arriere plan"

On regarde rapidement ensuite si les attaques ARP tournent bien en fond avec `ps aux | grep arpspoof`

### Commande arpspoof en rapide

arpspoof est un petit outil qui fait partie de la suite dsniff.
Quand on fait apt install dsniff, on récupère entre autres le binaire arpspoof.

Il fabrique et envoie des paquets ARP de type “reply” (op=2) sur le réseau, même si personne ne les a demandés.
Ces paquets contiennent :

une IP source (par ex. 172.18.0.4),

une MAC source (la tienne, 02:42:ac:12:00:02),

une IP de destination (172.18.0.3),

la MAC de destination (celle de la victime).

En gros :
arpspoof = un programme (de la suite dsniff) qui spam des trames Ethernet + ARP forgées pour manipuler la table ARP des autres machines.

## Resultat
<img width="895" height="232" alt="image" src="https://github.com/user-attachments/assets/cc4e3553-1317-43d7-b762-7ec4337d5130" />

On utilise tcpdump : Un outil qui écoute les paquets réseau qui passent sur ma machine.
Le `-A` affiche les paquets en ASCII
Le `port 3306` on ne veux écouter que MySQL, pas tout le réseau.

Vu qu on est en MITM actif , tout le trafic passe par nous, on voit tout en clair
Ca nous permet de voir toute la discussion entre le client et la bdd

handshake MySQL,login du client,envoi du nom d’utilisateur,envoi du mot de passe (sous forme hashée),requêtes SQL,réponses SQL

<img width="1041" height="191" alt="image" src="https://github.com/user-attachments/assets/81c69384-6e44-4c0c-92a4-3a392a57eedd" />

On arrive a choper la premiere partie du flag

## mdp de la bdd

Maintenant on dois reussir a recuperer le mdp root de la bdd

On installe hydra:

Hydra c’est un outil de bruteforce de mots de passe en ligne :

Il essaie plein de combinaisons login / mot de passe contre un service réseau :ssh, ftp, http, mysql, etc.

On a comme commande:

```
hydra -l root -P rockyou.txt 172.18.0.3 mysql

```
`hydra` l'outil de commande , `-l root` le login est fixé à root, `-P rockyou.txt` -P = fichier de Password list (Ici rockyou.txt) 
`172.18.0.3` la cible (IP du serveur MySQL dans notre cas) `mysql` le module / type de service que Hydra doit attaquer.

<img width="1089" height="264" alt="image" src="https://github.com/user-attachments/assets/239fe886-0e44-4576-a316-dcb6213f41de" />



















