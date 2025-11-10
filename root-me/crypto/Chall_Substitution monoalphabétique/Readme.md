## Contexte
Un personnage étrange vous contacte après avoir acheté un parchemin d’une provenance douteuse... Il compte sur votre esprit vif pour décrypter ce message ! Vous devrez déployer toutes vos facultés de cryptanalyse.

## Concept

Dans le fichier, le message est une suite de paires du type b3, a3, d1, etc.
Chaque mot est une suite de ces paires :

`b3a3d1 c2b1e3d4d3d1 a4e5c5b1e3c2a3d1 ...`   

Ça correspond exactement à un carré de Polybe 5×5, avec :

lignes codées par a b c d e  ,  colonnes codées par 1 2 3 4 5


|   | 1 | 2 | 3 | 4 | 5 |
|---|---|---|---|---|---|
| **a** | a | b | c | d | e |
| **b** | f | g | h | i | j |
| **c** | k | l | m | n | o |
| **d** | p | q | r | s | t |
| **e** | u | v | x | y | z |


[Télécharger le carré de Polybe (PDF)](./FR%20-%20Le%20carré%20de%20Polybe.pdf)

Donc par exemple :

`b3a3d1 → hcp`

## Decoder le polybe

On créer un petit script python qui viens nous decoder notre txt

[decoder_polybe.py](./decoder_polybe.py)


## Casser la substitution monoalphabétique

### Analyse de frequence
On donne le texte a DCODE, qui nous ressort le mapping des lettres:



Conserver les espaces : la substitution est monoalphabétique lettre→lettre.

substitution = {
    'a':'t','b':'j','c':'e','d':'o','e':'z','f':'r','g':'h','h':'c','i':'m',
    'j':'x','k':'q','l':'g','m':'b','n':'l','o':'v','p':'s','q':'i','r':'d',
    's':'n','t':'y','u':'p','v':'f','x':'a','z':'u'
}

### SCRIPT

On a plus qu'a faire un petit script python



