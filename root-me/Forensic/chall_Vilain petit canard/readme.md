
Ce challenge contenait un fichier .bin qui ne correspondait à aucun format connu. Les outils classiques (file, strings, binwalk) ne donnaient rien d’utile. C’est normal : ce type de fichier n’est pas un programme, mais une suite de codes clavier HID utilisés par des clés USB de type “Rubber Ducky”.

Un Rubber Ducky ne stocke aucun malware interne. Il se comporte comme un clavier et tape des commandes automatiquement sur la machine victime. C’est pourquoi le .bin ne contient que des scancodes (un octet pour la touche, un octet vide), ce qui explique le motif répétitif visible dans l’hexadump.

Pour analyser un fichier Rubber Ducky, il faut le décoder avec un outil adapté comme DuckToolkit. Le décodage révèle exactement les commandes que la clé aurait tapées : ici, des commandes PowerShell servant à télécharger un exécutable depuis un serveur distant, puis à l’exécuter.

L’analyse ne porte donc pas sur le .bin lui-même, mais sur l’exécutable téléchargé. Une fois le fichier récupéré, il suffit de l’examiner (par exemple avec strings) pour extraire le flag.

En résumé : un .bin très petit, sans structure identifiable, avec un motif “xx 00 xx 00” dans l’hexadump et aucune chaîne visible est presque toujours un script Rubber Ducky. Il ne contient pas de malware, seulement les instructions pour en télécharger un.
