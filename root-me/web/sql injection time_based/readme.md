

### Piege

J'ai d'abord foncé, en essayant sur la page login, mais malgré un bon nombre d'essaies rien
J'ai ensuite chequer la page membre, et on voit que dans l'url on a un parametre `member=1` , ce type de paramètre est souvent directement inséré dans une requête SQL sans protection

<img width="877" height="58" alt="image" src="https://github.com/user-attachments/assets/ed517a9a-e66b-4b21-8b8a-11c9c06eebfa" />

### SQLMAP

Ducoup, j'ai décidé d'utiliser SQLMAP, sauf que on doit être connecté sur Root-Me et récupérer notre cookie de session (PHPSESSID). Sans ce cookie, le serveur nous redirige vers la page de login.
Ensuite on creer un fichier que j'ai nommé basesql.txt

<img width="557" height="143" alt="image" src="https://github.com/user-attachments/assets/9928064b-ba76-4227-84c4-9bae60401bbc" />

**Le * après member=1 est crucial ! Il indique à SQLMap exactement où injecter. Sans lui, SQLMap va tester tous les paramètres et peut rater le bon.**

Ensuite on fait nos requette sqlmap:

La premiere:

`~/Documents » sqlmap -r basesql.txt --risk=3 --level=5 --batch --dbs --technique=T --dbms=PostgreSQL`

QUi va nous donner les bdd dispo, dans notre cas: SQLMap détecte que le paramètre member=1 est vulnérable et trouve la base 'public

La deuxieme:

<img width="1579" height="831" alt="image" src="https://github.com/user-attachments/assets/3882b9ee-40c1-43dd-8529-23500ec05fa4" />

On liste les tables presentes dans la bdd public

La troisieme:
Viens lister les contenus present dans la 

<img width="1364" height="34" alt="image" src="https://github.com/user-attachments/assets/23238373-4e9b-425e-b0c0-ffb655e11c90" />

<img width="937" height="119" alt="image" src="https://github.com/user-attachments/assets/5077ec72-d863-4f21-b1ae-53d32bbb5cd8" />







