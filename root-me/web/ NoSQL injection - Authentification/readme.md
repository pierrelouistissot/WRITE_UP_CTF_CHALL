### Fonctionnement

On est en NOSQL
On est sur un portail de login, 
Cependant, au lieu d’envoyer ces informations via un formulaire POST sécurisé, l’application les transmet directement dans l’URL en méthode GET

Cela révèle déjà deux éléments importants :

Les paramètres sont manipulables facilement.
L’application côté serveur interprète directement ces paramètres pour interroger une base de données.

On peut a premiere vue supposée que c est du mongodb  (?login=test&pass=test) par la facon dont les parametres sont structurés
Donc un utilisateur stocké pourrait ressembler a ca: 

```
{
  "login": "admin",
  "pass": "SuperSecret123"
}

```

L'authentification pourrait ressembler a ca:

```
db.users.find({
  login: "test",
  pass: "test"
});

```
Cela signifie :

“Cherche un utilisateur dont le login vaut ‘test’ ET le mot de passe vaut ‘test’.”

Si aucun document ne correspond, l’authentification échoue.
Si un document correspond, l’accès est accordé.

### Principe de MongoDB

MongoDB ne se limite pas à comparer des chaînes de caractères.
Il permet d’utiliser des opérateurs spéciaux, par exemple :

$eq → égal à

$ne → not equal (différent de)

$gt, $lt, etc.

On va donc utilisé cette **mechanique** la:

`{ login: { $ne: "toto" } }
`
Cela signifie :

“Tous les utilisateurs dont le login est différent de ‘toto’.”

### Premiere faille

J'ai rajouté les balise **[$ne]**

<img width="1240" height="147" alt="image" src="https://github.com/user-attachments/assets/0a4ff880-d4e4-42c7-bb08-45cff865aa12" />

On arrive à se co , a l'admin, ce qui se passe surement c est que mongodb regarde les utilisateurs differents de de test, test et prend le premiere donc l'admin

On doit donc trouver un moyen de faire des recherches parmis les users existants:
On a une balise en mongodb qui s'appele: [$regex] et qui permet de faire une recherche:
Docn notre payload ressemble mtn a ca:

<img width="1240" height="147" alt="image" src="https://github.com/user-attachments/assets/4876d576-a443-463f-b4e1-99a6177a6738" />

On fait ensuite toute les lettres possible
`
On trouve ca:

<img width="1240" height="147" alt="image" src="https://github.com/user-attachments/assets/eeed3ff2-fc72-4ea7-b880-802b27ae466e" />






