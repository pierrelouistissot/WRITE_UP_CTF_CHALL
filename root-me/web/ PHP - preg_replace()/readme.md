### preg_replace

On se renseigne sur la fonction:

<img width="635" height="271" alt="image" src="https://github.com/user-attachments/assets/11dcc69c-bb25-4665-99b8-a9b09f7127cf" />

On apprend qu'il ya  2,3 failles:

Deja il y a une faille `/e`

En gros ca c est un regex normal:

```
preg_replace('/a/', 'X', 'abc')  // => Xbc
```

Et nous on viens faire:

```
preg_replace('/a/e', 'X', 'abc')  // => Xbc
```

Grace a ca, le “replace” n’est plus un texte : il est interprété comme du PHP et exécuté.

### D'ou ca viens:

Dans un regex PHP, tu peux ajouter des modificateurs, apres le dernier /

| Regex      | Signification                                                |
| ---------- | ------------------------------------------------------------ |
| `/a/`      | cherche a                                                    |
| `/a/i`     | cherche A ou a (insensible à la casse)                       |
| `/a/s`     | modifie le comportement du `.`                               |
| **`/a/e`** | TRÈS DANGEREUX : **exécute le remplacement comme du PHP**    |  

### ARCHITECTURE

On peut imaginer que l'appli fait un truc du genre

```
echo preg_replace($_POST['search'], $_POST['replace'], $_POST['content']);
```
J'ai fais un premier test:


<img width="403" height="277" alt="image" src="https://github.com/user-attachments/assets/9e3a2ff8-3c74-4c4d-861d-d15083cfc98d" />


<img width="1324" height="687" alt="image" src="https://github.com/user-attachments/assets/fbfc9b4e-13b6-432d-8b07-e8c52b1ed398" />

On voit que `/e` fonctionne bien, ce qui c est passé, ducoup:

`preg_replace('/te/e', $_POST['replace'], "test");
`

dans le replace j'ai mit `phpinfo()`, ducoup le php fait ==> /te/e ==> je dois cherche `te` dans `test`, il trouve `te` et a la place, il execute phpinfo() comme du PHP


### Recup le flag

On utilise la fonction `file_get_contents`, pour recup les infos de flag.php

<img width="403" height="277" alt="image" src="https://github.com/user-attachments/assets/408ffbb8-c4bb-49c0-b259-00f1d4b62c08" />

L'appli nous ressort: ` <?php $flag="".file_get_contents(".passwd").""; ?> st`

Donc on execute la ligne qui se trouve dans flag.php

<img width="403" height="277" alt="image" src="https://github.com/user-attachments/assets/a225adfc-db75-400f-9233-fa278a1f33ff" />

On trouve ca: `pr3g_r3pl4c3_3_m0d1f13r_styl3`


