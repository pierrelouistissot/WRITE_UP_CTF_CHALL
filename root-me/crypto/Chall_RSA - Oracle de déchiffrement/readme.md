## Contexte

Énoncé
Vous avez réussi à intercepter un texte c, chiffré à l’aide d’une paire de clés RSA dont vous connaissez la composante publique (n,e).

Par chance, la victime a commis une maladresse en mettant à disposition un serveur permettant de déchiffrer n’importe quel texte chiffré avec sa clé publique, à l’exception de ceux représentant un secret devant rester en l’état.

À vous de le manipuler afin de déchiffrer ce mystérieux message !

n = 456378902858290907415273676326459758501863587455889046415299414290812776158851091008643992243505529957417209835882169153356466939122622249355759661863573516345589069208441886191855002128064647429111920432377907516007825359999
e = 65537
c = 41662410494900335978865720133929900027297481493143223026704112339997247425350599249812554512606167456298217619549359408254657263874918458518753744624966096201608819511858664268685529336163181156329400702800322067190861310616


## Rappel RSA

On choisit deux nombres secrets p et q (grands nombres premiers).

On calcule n=p*q 

On calcule φ(n) = (p-1)*(q-1)

On choisit un entier e tel que 1 < e < φ(n) et gcd(e, φ(n)) = 1

Cle publique (n,e) et la cle prive: d tel que e.d ≡ 1 (mod φ(n))

Chiffrement avec la cle publique c ≡ m^e (mod n)

Dechiffrement m ≡ c^d (mod n)

Propriété multiplier un ciphertext par S^e correspond à multiplier le plaintext par s après déchiffrement.

## Description précise du serveur

Le serveur est un oracle réseau (TCP) : si on lui envoie un ciphertext, il renvoie la décryption en clair sauf si le plaintext est exactement le secret.

On lui fournit un ciphertext , et le dechiffre avec sa cle prive RSA (il calcule m=c^d mod n)

Il vérifie si le plaintext obtenu correspond exactement au secret qu’il protège

Si le plaintext est le secret, il refuse de le renvoyer sinon, il affiche la valeur du plaintext sous forme d’un entier décimal (représentant m) puis redemande un autre ciphertext. 


Objectif : utiliser cet oracle pour obtenir quand même la décryption de c.

## Principe de l'attaque

On choisie un entier S tel que gcd(s,n)=1 (s inversible modulo n)

On cacule C'=C*S^e

Alors c' c est le chiffrement de m*s(mod n)

On l'envoie au serveur qui va nous dechiffrer c' et renvoye p=m*s

Ensuite on calcule s^(-1) modulo n pour obtenir m=p*s^-1(mod n)

Finalement on convertie m en bytes pour lire le flag

## Pratique

Pas besoin de prendre un gros S, on va prendre 2



