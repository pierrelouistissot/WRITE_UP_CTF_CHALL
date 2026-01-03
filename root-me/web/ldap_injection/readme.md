# LDAP Injection – Principes et Contexte

## 1. Qu’est-ce que LDAP

LDAP (Lightweight Directory Access Protocol) est un protocole utilisé pour accéder à un annuaire centralisé.  
Un annuaire LDAP est une base hiérarchique contenant des informations comme :

- utilisateurs
- groupes
- ordinateurs
- droits et attributs associés

LDAP est principalement utilisé dans les entreprises pour centraliser l’authentification et la gestion des identités.

---

## 2. Active Directory et LDAP

Active Directory (AD) est une implémentation Microsoft d’un annuaire d’entreprise.

Active Directory repose sur plusieurs protocoles :
- LDAP : lecture et recherche des informations (utilisateurs, groupes, droits)
- Kerberos : authentification par tickets
- DNS : localisation des services AD
- SMB / RPC : accès aux ressources et administration

LDAP est donc le **mécanisme de consultation** de l’annuaire, tandis que Kerberos gère l’authentification.

---

## 3. À quoi sert LDAP dans une authentification

Lors d’un login classique, le serveur :
1. reçoit un nom d’utilisateur et un mot de passe
2. construit un filtre LDAP
3. envoie ce filtre à l’annuaire
4. vérifie si une entrée correspond

Exemple de filtre LDAP d’authentification :

`(&(uid=USERNAME)(userPassword=PASSWORD))`


Si ce filtre retourne au moins une entrée, l’authentification est acceptée.

---

## 4. Structure d’un filtre LDAP

Les filtres LDAP utilisent une syntaxe logique :

- `&` : AND logique
- `|` : OR logique
- `!` : NOT
- `*` : wildcard (joker)
- `(` et `)` : délimitent les conditions

Exemples :

```
(uid=admin)
(uid=*)
(|(uid=admin)(uid=user))
(&(uid=admin)(userPassword=secret))

```


---

## 5. Qu’est-ce qu’une LDAP Injection

Une LDAP Injection se produit lorsque :
- une application construit un filtre LDAP avec des chaînes de caractères
- les entrées utilisateur ne sont pas filtrées ou échappées
- l’utilisateur peut modifier la logique du filtre

Exemple de code vulnérable (conceptuel) :

`filter = "(&(uid=" + username + ")(userPassword=" + password + "))"`




Dans ce cas, l’utilisateur contrôle directement une partie du filtre LDAP.

---

## 6. Différence avec une SQL Injection

LDAP Injection et SQL Injection reposent sur le même principe :
- l’utilisateur modifie la requête logique
- l’application exécute la requête modifiée

Correspondances logiques :

| SQL | LDAP |
|-----|------|
| OR | \| |
| AND | & |
| % | * |
| ' | ( ) |
| 1=1 | (uid=*) |

Il n’existe pas de commentaire en LDAP, contrairement à SQL.

---

## 7. Objectif d’une LDAP Injection sur une authentification

Dans la majorité des cas, l’objectif est :
- de forcer le filtre LDAP à retourner au moins une entrée
- sans connaître de mot de passe valide

Si le filtre retourne une entrée, l’application considère souvent que l’authentification est réussie.

---

## 8. Importance des messages d’erreur

Les erreurs LDAP sont extrêmement utiles pour un attaquant.

Exemple d’erreur :

`Invalid LDAP syntax : (&(uid=()(userPassword=test))`


Ce type d’erreur permet de :
- reconstituer le filtre LDAP exact
- comprendre où l’entrée utilisateur est injectée
- ajuster l’équilibre des parenthèses

Les erreurs LDAP agissent comme un leak de code.

---

## 9. Rôle du wildcard `*`

Le caractère `*` en LDAP signifie “n’importe quelle valeur”.

Exemples :

```
(uid=)
(userPassword=)
```


Ces expressions correspondent à presque tous les objets de l’annuaire.

Le wildcard est souvent utilisé pour transformer une condition stricte en condition permissive.

---

## 10. Pourquoi l’équilibre des parenthèses est critique

Les filtres LDAP doivent être syntaxiquement valides.
Contrairement à SQL, il n’existe pas de mécanisme de commentaire.

Toute injection LDAP doit :
- respecter l’équilibre des parenthèses
- produire un filtre complet et valide

Une injection correcte est souvent plus difficile à construire qu’en SQL.

---

## 11. Méthode générale d’analyse en CTF

Lorsqu’un formulaire utilise LDAP :

1. Tester des caractères spéciaux : `(`, `)`, `*`
2. Observer les messages d’erreur
3. Reconstituer le filtre LDAP
4. Comprendre où l’entrée utilisateur est injectée
5. Ajuster la logique sans casser la syntaxe
6. Rendre la requête permissive

---

## 12. Mesures de protection côté développeur

Pour éviter les LDAP Injections :
- échapper les caractères spéciaux LDAP (`*`, `(`, `)`, `\`, `NUL`)
- utiliser des APIs LDAP sécurisées
- ne jamais concaténer directement les entrées utilisateur
- limiter les messages d’erreur retournés au client

---

## 13. Conclusion

LDAP est un composant central des systèmes d’authentification d’entreprise.
Une mauvaise utilisation de LDAP peut permettre :
- un contournement d’authentification
- une élévation de privilèges
- une compromission de services internes

La LDAP Injection repose avant tout sur la compréhension de la logique des filtres, pas sur des payloads magiques.

