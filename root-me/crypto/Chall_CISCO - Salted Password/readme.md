## Context

L’administrateur réseau de votre entreprise a oublié ses mots de passes d’administration des routeurs. Il dispose cependant d’une sauvegarde de sa startup-config. À l’aide de celle-ci, retrouvez ses mots de passes !

Le flag est le mot de passe enable et le mot de passe administrateur concaténés.

## Resolution

On voit que dans le fichier on a: 2 strings retrouver
On voit dans le fichier 

<img width="524" height="318" alt="image" src="https://github.com/user-attachments/assets/f30eca7a-8eab-41a9-bc1e-185bd28dad2c" />

On voit par $1$ qu'on a du MD5

On met les hashs dans un fichier hash.txt a part
Puis on part en brut-force


