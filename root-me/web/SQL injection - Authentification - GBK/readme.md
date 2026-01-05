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


