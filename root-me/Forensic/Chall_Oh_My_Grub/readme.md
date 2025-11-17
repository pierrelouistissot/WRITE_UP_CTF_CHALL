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






<img width="485" height="133" alt="image" src="https://github.com/user-attachments/assets/179ab225-9471-4169-8ce4-7bc1aace4f1d" />




<img width="719" height="79" alt="image" src="https://github.com/user-attachments/assets/a61d8440-519d-4c54-b8cd-e7b867478d2f" />




<img width="1054" height="83" alt="image" src="https://github.com/user-attachments/assets/64497329-c7a9-47ed-9bcd-50505bf20311" />


<img width="551" height="251" alt="image" src="https://github.com/user-attachments/assets/aa3f1c81-4866-4bb3-bccd-ebd6b5d9ec5e" />

