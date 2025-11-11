## Contexte

Un message a été envoyé par une entreprise à deux de ses ingénieurs, mais elle a été négligente dans le choix des clefs de ses employés. Déchiffrez donc le message envoyé.

## Idee du chall

On a deux employés avec des clés publiques différentes, mais l’entreprise a été négligente :

même modulus n pour les 2 clés, exposant différent e1 et e2, même message

On a donc : 

C1=m^e1(mod n) et C2=m^e2(mod n)

Si gcd(e1,e2)=1 , alors il existe des entiers a et b tel que: ae1​+be2​=1

Alors on aurait: m=m^(ae1+be2)=((m^e1)^a) * ((m^e2)^b) = c1^a * c2^b (mod n)

**Donc on peut reconstruire directement m sans connaître la clé privée, juste avec les deux chiffrement et les deux exponents.**

## Analyse

<img width="484" height="628" alt="image" src="https://github.com/user-attachments/assets/3e651777-2cc3-4389-9e29-aa083f758cd9" />

Pour keypub1:

n=1024
e1=65537

Pour keypub2 :

n=1024
e=343223

## Code
```
import math
math.gcd(65537, 343223) 

```

gcd(e1,e2)=1 ==> attaque possible

```
import base64

c1 = int.from_bytes(base64.b64decode(open("message1","rb").read()), "big")
c2 = int.from_bytes(base64.b64decode(open("message2","rb").read()), "big")

```

Les fichiers message1 et message2 sont en base64. on les convertit en entiers

```
def egcd(a, b):
    if b == 0:
        return (1, 0, a)
    x, y, g = egcd(b, a % b)
    return (y, x - (a // b) * y, g)

a, b, g = egcd(e1, e2)  # e1=65537, e2=343223

```


On cherche a et b tq : ae1+be2=1

On trouve 133132e1-25421e2=1


```
def modinv(x, n):
    return pow(x, -1, n)  # Python 3.8+ : inverse modulaire

if a >= 0:
    part1 = pow(c1, a, n)
else:
    part1 = pow(modinv(c1, n), -a, n)

if b >= 0:
    part2 = pow(c2, b, n)
else:
    part2 = pow(modinv(c2, n), -b, n)

m = (part1 * part2) % n


```

On reconstruit le message m ==((c1)^a)*((c2)^b) (mod n)

Puis on convertie m en bytes puis en texte  et on trouve  le resultat!



