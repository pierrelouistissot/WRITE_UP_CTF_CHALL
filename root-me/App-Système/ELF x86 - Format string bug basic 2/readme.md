
```
#include <stdio.h>
#include <stdlib.h>
#include <sys/types.h>
#include <unistd.h>
 
int main( int argc, char ** argv )
 
{
 
        int var;
        int check  = 0x04030201;
 
        char fmt[128];
 
        if (argc <2)
                exit(0);
 
        memset( fmt, 0, sizeof(fmt) );
 
        printf( "check at 0x%x\n", &check );
        printf( "argv[1] = [%s]\n", argv[1] );
 
        snprintf( fmt, sizeof(fmt), argv[1] );
 
        if ((check != 0x04030201) && (check != 0xdeadbeef))    
                printf ("\nYou are on the right way !\n");
 
        printf( "fmt=[%s]\n", fmt );
        printf( "check=0x%x\n", check );
 
        if (check==0xdeadbeef)
        {
                printf("Yeah dude ! You win !\n");
                setreuid(geteuid(), geteuid());
                system("/bin/bash");
        }
}

```



### la vulnérabilité

`snprintf( fmt, sizeof(fmt), argv[1] );`

Pour rappel la fonction **snprintf**

int snprintf(char *str, size_t size, const char *format, ...);

In C, snprintf() function is a standard library function that is used to print the specified string till a specified length in the specified format.

Comme dans basic 1, si tu mets %x, %s, etc., snprintf va lire la pile en cherchant des arguments qui n’existent pas.

Mais ici, on va surtout utiliser %n, qui permet d’écrire en mémoire.

### Petit rappel

En c, %n en format string

```
int x = 0;
printf("AAAA%n\n", &x);

```
%n ne print rien
la place, il écrit dans x le nombre de caractères déjà imprimés avant lui.
ici "AAAA" → 4 caractères → x = 4

**Donc** si tu contrôles le format et tu arrives à faire en sorte que la pile contienne l’adresse d’une variable, tu peux dire à printf / snprintf :
“écris dans cette adresse le nombre de caractères imprimés jusque-là”

### Programme

`printf( "check at 0x%x\n", &check );`

On va donc executer une premiere fois le code, pour connaitre l'adresse de check:

<img width="449" height="95" alt="image" src="https://github.com/user-attachments/assets/29b10df6-ee81-4432-a132-9dc00abd5dc2" />


Ensuite on veut savoir quel “numéro d’argument” correspond à la zone de pile contrôlée par notre entrée (argv[1]).

<img width="973" height="93" alt="image" src="https://github.com/user-attachments/assets/bcf60b9e-f8af-4843-baeb-d96bb1ec2c0f" />


On cherche 41414141 dans ce qui est imprimé => c’est 0x41 = 'A' répété.

```
AAAA 
80485f1  ← %1$x
0        ← %2$x
0        ← %3$x
c2       ← %4$x
bffffc04 ← %5$x
b7fe1449 ← %6$x
f63d4e2e ← %7$x
4030201  ← %8$x   ← valeur de check = 0x04030201
41414141 ← %9$x   ← "AAAA" (0x41 0x41 0x41 0x41)
34303820 ← %10$x
31663538 ← %11$x
30203020 ← %12$x

```
### Pourquoi on ne peut pas ecrire DEADBEEF directement

%n écrit un int 32 bits = nombre de caractères imprimés.
0xDEADBEEF = 3735928559 en décimal → il faudrait imprimer 3,7 milliards de caractères

On utilise %hn, qui écrit un short (2 octets).
Un short va de 0 → 65535 → beaucoup plus simple.
0xDEADBEEF → haut 16 bits : 0xDEAD
              bas  16 bits : 0xBEEF

0xBEEF à l’adresse de check (&check)
0xDEAD à l’adresse &check + 2

<img width="1096" height="246" alt="image" src="https://github.com/user-attachments/assets/a89c9811-7a81-4b0c-965c-17a25b7462cb" />



