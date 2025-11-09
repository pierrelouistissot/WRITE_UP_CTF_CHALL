## Contexte
Lors d’un audit d’intrusion physique, vous parvenez à récupérer un téléphone d’un employé. Malheureusement, celui-ci est verrouillé par un schéma. Vous arrivez malgré tout à récupérer les fichiers du système.

Vous devez pour cette épreuve retrouver le schéma afin de déverrouiller le smartphone.

NB : Le mot de passe de validation est sous la forme d’une suite de chiffre.
(sha256 de l’archive : 525daa911d4dddb7f3f4b4ec24bff594c4a1994b2e9558ee10329144a6657f98)

## Observation

On a une archive système d’un Android verrouillé. L’objectif : retrouver le pattern (schéma) qui débloque l’écran.
Dans l’archive, il y a plein de fichiers système — mais seuls quelques-uns sont pertinents pour le verrouillage de l’écran.

Les fichiers importants que j’ai repérés :

<img width="714" height="586" alt="image" src="https://github.com/user-attachments/assets/6e75920a-859f-4725-b03a-0403671402a0" />


<img width="755" height="600" alt="image" src="https://github.com/user-attachments/assets/f865dfab-abce-41c0-804d-b90882f72c9d" />


En se renseignant on comprend que gesture.key c'est n binaire de 20 octets : c’est tout simplement le SHA-1 de la représentation binaire du motif (SHA-1 produit 20 octets)

La représentation binaire du motif est la suite d’octets contenant les indices des points visités, en ordre d’appui, chaque octet vaut 0..8 (0 pour la case en haut-gauche, 8 pour la case en bas-droite)

0 1 2
3 4 5
6 7 8

On peut recuperer directement le sha-1 du gesture.key parce que un sha ne s'inverse pas (impossible mathematiquement)

PAR CONTRE: Le nombre de motif valide est "PETIT" on a environ (389 112 motifs possibles pour longueurs 4..9)
On peut donc brute-forcer


## Règles exactes d’un motif Android (pour générer les candidats)
Pour faire le code de brute force, on doit s'assurer de bien comprendre les regles:

  Taille: min=4 & max=9
  Unicité des points: chaque point (case) ne peut être utilisé qu’une seule fois dans un motif.
  Règles de saut / « middle node » : Si on veut aller d’un point A à un point B et que il existe un point M exactement entre A et B (c’est-à-dire A — M — B en ligne droite), alors tu peux faire le saut A→B uniquement si M a déjà été utilisé                précédemment dans le motif.

  On va donc faire un code python pour exploiter tout ca

## Comment le code cherche le bon schéma

On peut voir le programme comme un petit robot qui explore tous les chemins possibles :

1. Il choisit un point de départ (0, 1, 2, ..., 8).
2. À partir de ce point, il essaie d’ajouter un autre point, en vérifiant à chaque fois si :
   - le point n’a pas déjà été utilisé,
   - le mouvement respecte la règle du "milieu".
3. À chaque fois que la longueur du motif est d’au moins 4 points, il :
   - transforme la liste `[1,4,5,2,...]` en bytes,
   - calcule le SHA-1 de ces bytes,
   - compare ce SHA-1 avec le contenu de `gesture.key`.
4. Si ça correspond, il s’arrête et affiche le motif trouvé.
5. Sinon, il "annule" le dernier point (c’est le principe du **backtracking**) et essaie un autre chemin.

Cette exploration est faite avec une fonction récursive (`try_extend_pattern`), qui :
- reçoit le motif en cours (`current_pattern`),  
- l’ensemble des points déjà utilisés (`used_points`),  
- et la valeur cible (`target_hash` = contenu de `gesture.key`).

  

  
