## Contexte


On à un fichier : root.ova
Le scénario dit que la société a perdu l’accès à un serveur important.
Un fichier .ova correspond à une machine virtuelle exportée.

Donc, ce qu'on a entre les mains, c’est le disque dur d’un serveur sous forme de fichier.

Pas besoin d’allumer la VM. Pas besoin d’avoir les mots de passe.

En forensic, on monte directement le disque et on lit tout.

### C'est quoi un fichier ova

.ova(Open Virtual Appliance) ==> C est une archive TAR qui contient un fichier (ovf=> description de la vm) et un fichier (.vmdk=> disque dur de la vm)


Donc la premiere etape qu'on fait c'est de l'extraire comme un zip:

<img width="457" height="72" alt="image" src="https://github.com/user-attachments/assets/c4472739-0166-4db3-8d9d-df1fbe684dc0" />


On va egalement convertir le vmdk en raw:

<img width="628" height="21" alt="image" src="https://github.com/user-attachments/assets/c301ba19-b551-42d3-badd-d183c63a4c98" />


En forensic, on travaille presque toujours avec des disques en format RAW.
C’est le format le plus simple possible : un fichier binaire qui correspond bit à bit à un disque.

On va ensuite monter le disk et tout afficher:

<img width="707" height="227" alt="image" src="https://github.com/user-attachments/assets/3f146140-6af5-4478-b6e0-eab7aadc5f7b" />

disk.raw1 = la partition principale Linux 

Attention tricky:

Quand tu montes un disque RAW, tu dois dire à Linux où commence la partition.

Le début de disk.raw1 est au secteur 2048.
Un secteur = 512 octets.


2048 * 512 = 1048576 la partition commence à l'octet 1048576 soit exactement 1 Mo.

Ensuite on vient monter la partition:

<img width="702" height="40" alt="image" src="https://github.com/user-attachments/assets/975facb8-4671-40b2-a410-a63c9939f536" />


Et ensuite on se balade dedans:

<img width="1032" height="38" alt="image" src="https://github.com/user-attachments/assets/80dbd73c-0f10-4e00-ae32-fb5000ff8e5c" />




<img width="551" height="251" alt="image" src="https://github.com/user-attachments/assets/aa3f1c81-4866-4bb3-bccd-ebd6b5d9ec5e" />

