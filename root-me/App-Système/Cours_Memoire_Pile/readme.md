


<img width="841" height="483" alt="image" src="https://github.com/user-attachments/assets/a3601d01-051f-4ea5-ac54-b54ae063ffc1" />

### On retrouve les 3 sections suivantes :

#### Texte (.text) Données (.data) bss (.bss)

Rapidement, la première **section texte (.text)** est celle qui contient le code du programme, et plus exactement les instructions en langage machine. C’est une section en lecture seule, une fois qu’elle a été définie, elle est immuable. Elle sert seulement à stocker du code, pas des variables. Des erreurs de programmation peuvent entraîner cette fameuse erreur : “Segmentation Fault”, qui indique à l’utilisateur qu’une écriture non autorisée a tenté d’être faite dans cette zone mémoire.


La section de **données (data) et la section bss** stockent les variables globales et statiques du programme. Si ces données sont initialisées, elles sont enregistrées dans la section data, tandis que les autres sont dans la section bss. Ce sont également des zones mémoires de taille fixe. Malgré la possibilité en écriture, les variables finales et statiques ne changeront pas au cours de l’exécution du programme ou du contexte.


### 2 zones memoires suivante

#### tas(heap) & pile(stack)

**Le tas (heap)** est, quant à lui, manipulable par le programmeur. C’est la zone dans laquelle sont écrites les zones mémoires allouées dynamiquement (malloc() ou calloc()). Tout comme la pile, cette zone mémoire n’a pas de taille fixe. Elle augmente et diminue en fonction des demandes du programmeur, qui peut réserver ou supprimer des blocs via des algorithmes d’allocation ou de libération pour une utilisation future. Plus la taille du tas augmente, plus les adresses mémoires augmentent, et s’approchent des adresses mémoires de la pile.

Par ailleurs, les variables stockées dans le tas sont accessibles partout dans le programme, par l’intermédiaire des pointeurs. Cependant, l’accès aux variables stockées dans le tas ne se faisant qu’avec des pointeurs, cela ralentit un peu ces accès, contrairement aux accès dans la pile.

**La pile (stack)** possède également une taille variable, mais plus sa taille augmente, plus les adresses mémoires diminuent, en s’approchant du haut du tas. C’est ici qu’on retrouve les variables locales des fonctions ainsi que le cadre de pile (stack frame) de ces fonctions. La stack frame d’une fonction est une zone mémoire, dans la pile, dans laquelle toutes les informations, nécessaires à l’appel de cette fonction, sont stockées. S’y trouvent également les variables locales de la fonction.

### Registres:

Le processeur x86 32 bits possède (logiquement) 8 registres généraux (EAX, EBX, ECX, EDX, ESP, EBP, ESI, EDI)

Pour les processeurs 64 bits, il y a 16 registres logiques. Mais dans la réalité, les derniers processeurs en ont 168, pour pouvoir paralléliser les instructions.

Les 4 **EAX, EBX, ECX et EDX** appelés Accumulateur, Base, Compteur, Données ont pour rôle de stocker des données temporaires pour le processeur lorsqu’il exécute un programme.

Les 4 autres registres **ESP, EBP, ESI et EDI**  appelés Pointeur de Pile (Stack), Pointeur de Base, Index de Source et Index de Destination sont plutôt utilisés en tant que pointeurs et index, comme leur nom l’indique.


## Fonctionnement de la pile

La pile a une structure **LIFO** (Last In, First Out).
Cela veut dire que **le dernier élément qui est placé sur la pile sera le premier élément à être dépilé.**
la stack empile ses éléments vers le bas.
Donc ce qu’on appelle le haut de la stack, c’est finalement l’adresse la plus basse de la stack. Plus on empile des valeurs dans la stack, plus les adresses diminuent.


**stack frame**  les informations stockées sur la pile lors de l’appel d’une fonction pour enregistrer le contexte d’exécution ainsi que les variables passées à la fonction

Le registre ESP garde en mémoire l’adresse du haut de la pile (donc l’adresse la plus basse, puisque plus la pile grandit, plus les nouvelles adresses sont basses).Il est donc mis à jour à chaque modification de la pile (ajout d’une valeur ou suppression de la dernière valeur).
Le registre EBP garde en mémoire l’adresse du début de la stack frame. Ainsi, la stack frame courante se situe entre l’adresse contenue dans EBP et l’adresse contenue dans ESP.

Voici un schéma qui illustre le rôle des registres EBP et ESP :

<img width="936" height="456" alt="image" src="https://github.com/user-attachments/assets/877f57de-406c-4ad2-8359-3b249de80f72" />







