```
#include <stdio.h>
#include <string.h>
#include <sys/types.h>
#include <unistd.h>
 
int main (int argc, char ** argv){
    char message[20];
 
    if (argc != 2){
        printf ("Usage: %s <message>\n", argv[0]);
        return -1;
    }
 
    setreuid(geteuid(), geteuid());
    strcpy (message, argv[1]);
    printf ("Your message: %s\n", message);
    return 0;
}

```

## La faille

```
char message[20];
...
strcpy(message, argv[1]);

```

La faille est ici
message fait 20 octets.
strcpy ne vérifie pas la taille de la chaîne source (argv[1]), donc si on passe un argument plus long que 19 charactere on va deborder sur le buffer.
Comme le code fait `setreuid(geteuid(), geteuid());` ca veut dire qu'il tourne avec les droits du proprietaire
Donc si on controle l'adresse de retour `EIP` et faire en sorte que `system("/bin/sh") soit appelée`, on peut faire en sorte d'obtenir un shell avec les droits du programme

## Comment faire
 On veut savoir combien d'octets il faut pour ecraser EIP
 Pour cela on lance le programme avec gdb et on fait run  $(python -c 'print("A"*32)')
 
 <img width="1100" height="350" alt="image" src="https://github.com/user-attachments/assets/8624bf4f-e0df-4fa9-abef-1a51c182bb89" />

 On trouve un offset de 32

  Ensuite on vient prendre les adresse de system() et exit() qui viennent de la libc = la bibliothèque standard du C
  Le programme est compilé en utilisant cette bibliothèque, donc la libc est chargée en mémoire au lancement du programme.

system(<string>) exécute une commande shell, donc system("/bin/sh") lance un shell interactif.
Et comme ton programme est SUID/setreuid => ton shell aura les droits du binaire

Donc la on va faire en sorte que le ret de main saute directement à system.
Donc on va fabriquer la pile à la main pour qu’au moment où main fait ret, la pile ait exactement le format attendu par system.

## Rapide principe

EIP = Extended Instruction Pointer
C’est LE registre qui contient l’adresse de la prochaine instruction machine que le CPU va exécuter

Quand en C on fait `system("/bin/sh");`, le compilateur genere un **call system**
Un call fait 2 choses:

-push l’adresse de retour sur la pile
-met EIP à l’adresse de system()

Donc apres un call system on a `EIP = adresse_de_system`


Maintenant EIP dans un overflow :

[ buffer ]
[ EBP sauvegardé ]
[ EIP sauvegardé ]  <-- ce qu’on écrase !


## Payload

<img width="1098" height="106" alt="image" src="https://github.com/user-attachments/assets/1434709d-a9f1-4978-98ae-0f2b6656a09f" />

 
