<img width="788" height="727" alt="image" src="https://github.com/user-attachments/assets/d333ce87-0fec-4430-8b44-10c42322ff84" />

On saute le ptrace, ca demande un mdp

On ouvre ghidra, on trouve ca:



<img width="541" height="673" alt="image" src="https://github.com/user-attachments/assets/8b1f212b-957e-4c98-b47a-c299cecff9a8" />

On pense alors a un system clé / password reconstruit en mémoire.

On doit donc trouver la chaine de charactere:

J'ai d abord essayer avec des strcmp mais je ne trouvais rien, ducoup j'ai fait:

Ducoup:

j'ai check le flux autour des messages :

si mauvais : puts("Wrong password! Try again.")

si bon : puts("Good Job! Here is your flag:") puis appel à la routine du flag

Dans le désassemblage du main, on voit un appel à une fonction de vérification :

call 0x555555555270

puis test eax, eax

si eax == 0 ==> branche “Wrong password”

sinon ==> branche “Good job” et appel du flag

ON check la fonction on voit qu'elle genere 12 octes, elle impose une longueur exacte de 12 caractèrs, et elle compare le buffer généré à l’entrée utilisateur


Ensuite, la comparaison ne se fait pas via strcmp, mais via comparaison brute en mémoire et c est ca qui m a bien bz:

comparaison des 8 premiers octets :

mov (%rsp),%rax
cmp %rax,(%rbx)


puis comparaison des 4 suivants :

mov 0x8(%rsp),%eax
cmp %eax,0x8(%rbx)


Une fois qu’on a compris que le password est construit à $rsp, adresse clé est :

0x5555555552f1

<img width="902" height="134" alt="image" src="https://github.com/user-attachments/assets/6e73dbfe-159a-44cd-a1d8-0b726be27750" />

DOnc le mot de passe est passw0rd123!


<img width="341" height="81" alt="image" src="https://github.com/user-attachments/assets/45ec5cb4-ee5e-4d21-bce8-cd5f0bf67a05" />
