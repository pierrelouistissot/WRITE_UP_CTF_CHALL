### But du défi


Ce challenge repose sur une authentification en PHP basée sur des données JSON envoyées en POST :
On a accés au code php de la page:

<img width="930" height="350" alt="image" src="https://github.com/user-attachments/assets/ec7b5f76-dc30-47a4-a87f-94644fc0f084" />

La partie qui nous interesse c'est celle la:

```
if ($auth['data']['login'] == $USER 
    && !strcmp($auth['data']['password'], $PASSWORD_SHA256)) {
    $return['status'] = "Access granted! The validation password is: $FLAG";
}

```


### Php comparateur

<img width="1042" height="477" alt="image" src="https://github.com/user-attachments/assets/98a9b29a-4c05-427c-b3a3-cd2528af59eb" />


<img width="1042" height="477" alt="image" src="https://github.com/user-attachments/assets/2de2635e-3ffc-4a65-b6ea-08ac82adf49d" />

On a `===` qui est un comparateur strict et `==` qui est un comparateur chill

PHP peut considérer des choses très différentes comme “égales”, ce qui ouvre la porte au type juggling.

Dans ce chall: `$auth['data']['login'] == $USER`

On egalement strcmp: strcmp(a, b) est censé comparer deux chaînes de caractères et renvoie :

<img width="1027" height="128" alt="image" src="https://github.com/user-attachments/assets/4abe4cb9-13dd-4309-bf65-8af1fb6fbf3f" />


```
strcmp("admin", "admin")  // → 0
strcmp("admin", "root")   // → 5 (ou -5)
strcmp([], "admin")       // → NULL  ← comportement exploitable

```

### Exploitation

#### Login

`$auth['data']['login'] == $USER `

Si $USER = "admin", il suffit d’envoyer "admin".

#### Password

`!strcmp($auth['data']['password'], $PASSWORD_SHA256) `

pourquoi `!`:

| Valeur     | Interprétation |
| ---------- | -------------- |
| `0`        | false          |
| nombre ≠ 0 | true           |
| `NULL`     | false          |

Donc:

| Cas                  | `strcmp()` | `!strcmp()`           |
| -------------------- | ---------- | --------------------- |
| Bon mot de passe     | `0`        | `true`               |
| Mauvais mot de passe | `123`      | `false`              |
| **Tableau `[]`**     | `NULL`     | **`true`  (bypass)** |


### Resolution


J'ai teste pas mal de chose:

D'abord j'ai fait login:admin et password:[]
Mais ca ne marchée pas, je pensais que ma logique n'etais pas bonne pour le password
J'ai ducoup verifier, en faisant un programme en php ca me sortait bien true quans je faisais un `!strcmp([12203],password)`, car ==> strcmp([12203],password)=null et donc !strcmp==>true, 

ENfaite la faute etait dans le login, j'ai donc modif pour mettre 0 a la place de `admin` et la ca à fonctionnait:
Pour moi la logique derriere c est:

"admin" converti en nombre ==> 0 (car ce n’est pas un nombre)

donc : 0 == "admin" ==> true

<img width="1312" height="455" alt="image" src="https://github.com/user-attachments/assets/3ce77cbc-164c-4e9a-9db4-b1ab64676885" />








