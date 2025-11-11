## Contexte

Un message a été envoyé par une entreprise à deux de ses ingénieurs, mais elle a été négligente dans le choix des clefs de ses employés. Déchiffrez donc le message envoyé.

## Idee du chall

On a deux employés avec des clés publiques différentes, mais l’entreprise a été négligente :

même modulus n pour les 2 clés, exposant différent e1 et e2, même message

On a donc : 

C1=m^e1(mod n) et C2=m^e2(mod n)

Si on arrive a trouver a et b tel que: ae1​+be2​=1

Alors on aurait: m=m^(ae1+be2)=((m^e1)^a) * ((m^e2)^b) = c1^a * c2^b (mod n)

**Donc on peut reconstruire directement m sans connaître la clé privée, juste avec les deux chiffrement et les deux exponents.**
