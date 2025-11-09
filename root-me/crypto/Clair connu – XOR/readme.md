## Contexte
Objectif : analyser un fichier (supposé être un BMP chiffré par XOR) et récupérer la clé pour décrypter l’image.

## Analyse initiale
On commence par regarder les caractéristiques connues d’un fichier BMP non chiffré :

<img width="658" height="213" alt="image" src="https://github.com/user-attachments/assets/3fb561c5-725a-4601-a7d9-982b5f341307" />

On a donc les premiers octet en hexadecimal du fichier: 

Maintenant on sait que dans un fichier BMP non chiffré normalement: 

Octet 0: 0x42(B) 

1:0x4D(M) 

10..13 = 0x36 0x00 0x00 0x00 (offset des pixels = 54) 

14..17 = 0x28 0x00 0x00 0x00 (taille DIB = 40) 

Ces valeurs sont connues et fixes dans la plupart des BMP. On va les utiliser pour retrouver la clé. 

On sait que soit C un octet chiffré et P un octet clair alors: 

Clé=C XOR P, car XOR est reversible (A XOR B =C ==> C XOR A = B) 

Donc: 

Pour la position 0: 

C:0x24 P:0x42 ==> cle[0]=0x24 XOR 0x42=0x66==’f’ 

Pour la position 1: 

C: 0x2c P=0x4d ==> cle[1]= 0x2c XOR 0x4d=0x61==’a’ 

 

On sait donc que la clé commence par ‘fa’ 

On continue avec les autres que l’on connait  cad: 10 a 17 

On obtient: [10:’e’|11:’n’|11:’f’|12:’a’|13:’l’|14:’l’|15:’e’|16:’n’|17:’f’] 

On remarque que le partene ce repete, on a ‘fallen’, on a la clé 


<img width="659" height="124" alt="image" src="https://github.com/user-attachments/assets/403e0987-1638-4c6e-8026-6a177cc93617" />


LE FICHIER DECRYPTED DONNE: 

## Resultat

<img width="632" height="481" alt="image" src="https://github.com/user-attachments/assets/7007ee1d-8341-432e-a575-76c27881aa90" />


