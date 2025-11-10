## Contexte

Énoncé
Voici une archive contenant un fichier chiffré, et le programme ayant été utilisé pour le chiffrement. Votre objectif est de récupérer le contenu de ce fichier en clair.

Indice : D’après nos informations, le fichier aurait été chiffré lors du mois de décembre 2012.

## Decouverte

### Comprendre le code C donné


 ```
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>

#define KEY_SIZE 32
#define BUFF_SIZE 1024

unsigned int holdrand = 0;
 ```
`#define KEY_SIZE 32`==> la taille de la clé de chiffrement sera 32 caractères.
`#define BUFF_SIZE 1024`==>on va lire le fichier par morceaux de 1024 octets.

```
static void Srand (unsigned int seed) {
  holdrand = seed;
}

static int Rand (void) {
  return(((holdrand = holdrand * 214013L + 2531011L) >> 16) & 0x7fff);
}

```
`Srand` recoit un entier, la seed, la valeur de depart

la variable `holrand` prend la valeur de seed

Plus tard dans le `main` il fera `Srand(time(NULL));`==>la valeur de départ vient de l’horloge (le nombre de secondes depuis 1970).

`Rand`:fonction calcule la prochaine valeur de holdrand

On prend la valeur de holrand, on l' a multiplie par 214013L, on ajoute 2531011, ca nous donne la nouvelle valeur de holrand

Puis on décale cette valeur de 16 bits vers la droite puis on garde seulement les 15 bits du bas avec le mask & 0x7fff.


Au final, Rand() renvoie un entier entre 0 et 32767, et chaque nouveau nombre de rand() depend du precedent, donc de seed...

*DONC ON VEUT CONNAITRE SEED*

```
char* genere_key(void) {
  int i;
  static char key[KEY_SIZE+1];
  const char charset[] = 
    "abcdefghijklmnopqrstuvwxyz"
    "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    "123456789";
  
  for(i = 0; i < KEY_SIZE; i++) {
    key[i] = charset[Rand() % (sizeof(charset) - 1)];
  }
  key[KEY_SIZE] = '\0';

  return key;
}

```

Le gros de cette partie , c est la boucle:

```
for(i = 0; i < KEY_SIZE; i++) {
  key[i] = charset[Rand() % (sizeof(charset) - 1)];
}
```
On appelle Rand(), ça donne un nombre entre 0 et 32767.

On fait % (sizeof(charset) - 1) pour le ramener dans la plage [0, longueur_charset-1]

On prend le caractère correspondant dans charset, ça donne un caractère “pseudo-aléatoire”.

On repete ca 32 fois


```
void crypt_buffer(unsigned char *buffer, size_t size, char *key) {
  size_t i;
  int j;

  j = 0;
  for(i = 0; i < size; i++) {
    if(j >= KEY_SIZE)
      j = 0;
    buffer[i] ^= key[j];
    j++;
  }
}

```
Le but de la fonction c est de parcourir le contenu du buffer octet par octet et applique un XOR avec la clé.
Mais comme la clé ne fait que 32 caractères, on la répète autant de fois que nécessaire.
Le `buffer` c est les données de notre fichier a chiffrer

Donc size ca va etre le nombre d'octets a traiter
Donc on a dans la boucle for:
`buffer[i]` contient un octet du fichier
`key[j]` un octet de la clé
`buffer[i] ^= key[j];` remplace `buffer[i]` par `buffer[i] XOR key[j]`

```
void crypt_file(FILE *in, FILE *out) {
  unsigned char buffer[BUFF_SIZE];
  char *key;
  size_t size;

  key = genere_key();

  printf("[+] Using key : %s\n", key);

  do {
    size = fread(buffer, 1, BUFF_SIZE, in);
    crypt_buffer(buffer, size, key);
    fwrite(buffer, 1, size, out);

  } while(size == BUFF_SIZE);  
}
```

C’est cette fonction qui lit le fichier d’entrée et qui écrit dans le fichier chiffré.
Mais elle ne lit pas tout le fichier d’un coup.
Elle lit par petits bouts de 1024 octets, qu’elle chiffre un à un.

`key = genere_key();`

On génère une clé aléatoire de 32 caractères.
Elle servira à chiffrer tout le fichier (la même clé pour chaque bloc).

`fread(buffer, 1, BUFF_SIZE, in);`

On lit jusqu’à 1024 octets du fichier d’entrée.

`crypt_buffer(buffer, size, key);`

On chiffre ce bloc avec la clé.

C’est ici qu’on appelle la fonction qu’on vient d’expliquer.

`fwrite(buffer, 1, size, out);`

On écrit les octets chiffrés dans le fichier de sortie.

`while(size == BUFF_SIZE)`

Tant qu’on a lu un “bloc complet” de 1024 octets, on continue la boucle.

Quand on arrive à la fin du fichier, fread renvoie un nombre plus petit,la boucle s’arrête.


Maintenant qu'on a compris le code on peu comprendre ces faiblesses:

## Faiblesse

La clé dépend uniquement de time(NULL) donc du moment précis où le fichier a été chiffré.
Si on sais à peu près la date (décembre 2012, donné dans la consigne), on peux tester toutes les secondes de ce mois pour retrouver la clé exacte.

Le chiffrement est juste un XOR → facile à inverser si on retrouve la clé.

Résultat :
Avec le code du programme, le fichier .crypt, et la date approximative,
tu peux retrouver la même clé et déchiffrer tout le fichier.

## Ce qu'on fait


On va faire un script python qui reproduit le meme generateur de nombre
```
holdrand = (holdrand * 214013 + 2531011) & 0xffffffff
rand = (holdrand >> 16) & 0x7fff
```
Meme genenre_key(), prendre 32 nombre genere par Rand(), faire un %len(charset) pour choisir une lettre dans `abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ123456789`
et concatene les 32 lettres

On sait egalement que e fichier s’appelle *.bz2.crypt ==> donc c’est sûrement un fichier bzip2
Et d'apres la documentation les fichiers bzip2 commencent toujours par **BZh**

### Principe

Donc on peut partir du principe que si après dechiffrement le fichier commence par BZh, alors on a trouvé la bonne clé





