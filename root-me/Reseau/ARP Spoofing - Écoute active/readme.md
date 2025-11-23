
## Contexte

Après lancement du challenge, on se connecte en SSH sur la machine fournie :
```
ssh -p 22222 root@ctf05.root-me.org

```

Le système est une Ubuntu minimaliste, réduite au strict nécessaire.
On doit donc nous-mêmes installer certains outils pour analyser le réseau.

L'objectif global du challenge est de réaliser une attaque ARP Spoofing pour se placer en Man-In-The-Middle et intercepter une requête contenant des informations sensibles.

### Comprendre l'environnement

<img width="700" height="315" alt="image" src="https://github.com/user-attachments/assets/12926337-be7a-4a9d-8bd3-c1d3308563fe" />

### Interpretation

ifconfig, nous montre 2 interfaces:

l’interface eth0

l’interface lo (loopback==> le, receveur et l'envoyeur sont les memes)

On comprend que :

Notre machine a l’adresse 172.18.0.2
Le masque 255.255.0.0 indique un réseau en /16
donc le LAN s’étend de 172.18.0.0 à 172.18.255.255

**Avant un ARP Spoof, on doit connaître notre IP et notre interface, pour pouvoir sniffer le trafic ou lancer l’empoisonnement ARP sur la bonne interface.**

On verifie le cache ARP local

<img width="491" height="35" alt="image" src="https://github.com/user-attachments/assets/5edc37e2-977c-415f-996f-629b214d060d" />

### Interpretation

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









