On nous donne accés au code source de la page, et notamment au PHP qui gére le login:

Revoir le php-juggling, mais on voit bien qu'il y aura un probléme dans cette section:


```
// autologin cookie ?
else if($_COOKIE['autologin']){
    $data = unserialize($_COOKIE['autologin']);
    $autologin = "autologin";
}

// check password !
if ($data['password'] == $auth[ $data['login'] ] ) {
    $_SESSION['login'] = $data['login'];

```

La ligne  `$data = unserialize($_COOKIE['autologin']);` ==> Désérialiser un cookie = Prendre le texte stocké dans le cookie ==> Le transformer en objet utilisable par l’application
Le serveur désérialise directement le cookie sans validation, puis compare le mot de passe. Et la comparaison utilise == (loose comparison) et non === (strict comparison)

On voit un peu pres les attaques a faire:

### PHP-Juggling

Si on met password = 0 (entier), alors 0 == $auth['superdamin'] sera TRUE car PHP convertit la string du vrai mot de passe en entier lors de la comparaison

ON test ducoup, on se connecte avec guest guest, on click sur reste connecte, puis quand on reviens en arriere, on observe ca:

<img width="1415" height="196" alt="image" src="https://github.com/user-attachments/assets/27d57fd4-61dc-4dbb-aff9-a0a9bb3fcecd" />

On a un cookie "AUTOLOGIN" , on regarde ca structure sur burp:

<img width="524" height="196" alt="image" src="https://github.com/user-attachments/assets/b9d2d870-b63f-4da4-8dc6-46efd9e72d9a" />

On capte la forme:

`a:2:{s:5:"login";s:5:"guest";s:8:"password";s:64:"84983c60..."}`

C'est un tableau PHP sérialisé. On comprend le format :

Dans le code source on a vu:

```
if($_SESSION['login'] === "superadmin"){
    require_once('admin.inc.php');
}
```

Il faut se faire passer pour `superadmin`.`

On forge donc le cookie malveillant :

On forge un tableau sérialisé avec :
- `login = "superadmin"` (10 chars → `s:10`)
- `password = true` (booléen → `b:1`)
```
a:2:{s:5:"login";s:10:"superadmin";s:8:"password";b:1;}
```

Avant de trouver `b:1`, j'ai teste `i:0`,`i:2`, s:0:"", et au final c est b:1 qui fonctionne:

Enfaite je sais pas pourquoi les autres ne marchent pas, mais b:1 c est logique:

La comparaison :

true == $auth['superadmin']

$auth['superadmin'] = "5e884898..." (hash sha256, string non-vide)

string non-vide ==> true en booléen

Donc : true == true ==> TRUE


<img width="1822" height="643" alt="image" src="https://github.com/user-attachments/assets/5bd4a638-b6ea-4435-9173-0812690a9a68" />

