## Contexte

Retrouvez le mot de passe permettant de valider ce challenge.

<img width="1084" height="34" alt="image" src="https://github.com/user-attachments/assets/33d72e15-23c5-43e0-8cd2-37a835a141df" />


ELF 64 bits : exécutable Linux classique.

x86-64 : architecture 64 bits.

<img width="478" height="74" alt="image" src="https://github.com/user-attachments/assets/fa5f405b-445a-48ca-a910-ff6fb650b8eb" />

On voit que dans les permissions il manque le "x"

On fait donc un `chmod +x ch32.bin`

<img width="418" height="104" alt="image" src="https://github.com/user-attachments/assets/d145dd61-3dcb-46a8-a6ce-8a225ff8920b" />

On fait ensuite un `strings ch32.bin`

<img width="161" height="40" alt="image" src="https://github.com/user-attachments/assets/31636efd-c6c2-46eb-b501-fe3b7b0c80bd" />

main.main c'est la vrai fonction main en go.

On va donc regarder dans le Decompileur Ghidra:

<img width="739" height="616" alt="image" src="https://github.com/user-attachments/assets/4fa3a93f-b55c-456f-a27c-5576d5a64141" />

_DAT_00000010 = adresse où se trouvent les caractères de la chaîne.

_DAT_00000018 = adresse d’un entier qui contient la longueur.

Pour essayer de trouver la chaine, on double click sur les variable mais on a rien

On regarde le listing:

<img width="688" height="124" alt="image" src="https://github.com/user-attachments/assets/3cd9fb00-6129-4d7e-9b5e-6711660ecfb8" />

J'essaye de double clicker sur DAT_004c446D, et on trouve ca:


<img width="422" height="167" alt="image" src="https://github.com/user-attachments/assets/ee8dbb00-8d5f-49d0-8702-61a6a9a9c33d" />

BAMMM, je pense on a la clef


<img width="726" height="264" alt="image" src="https://github.com/user-attachments/assets/6b14b57e-7f33-4955-bc72-f5ebbe5c2024" />

pbVar4 → pointeur vers le caractère courant de mon input.

local_48 → pointeur vers la clé.

uVar5 → index i dans l’input.

uVar3 → index i % len(key) dans la clé.

mon mot de passe est XORé avec la clé , et le résultat est comparé à un tableau constant.

Le tableau le voici:

<img width="452" height="166" alt="image" src="https://github.com/user-attachments/assets/a60e056d-70f7-4caa-8f83-a24b011e4edd" />


L’étape qu’on a faite à côté pour retrouver le mot de passe, c’est juste inverser le XOR :

`input[i] = secret[i] ^ key[i % len(key)]`

On trouve : le mdp, gg















