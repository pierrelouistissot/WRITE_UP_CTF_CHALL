## Context

L’administrateur réseau de votre entreprise a oublié ses mots de passes d’administration des routeurs. Il dispose cependant d’une sauvegarde de sa startup-config. À l’aide de celle-ci, retrouvez ses mots de passes !

Le flag est le mot de passe enable et le mot de passe administrateur concaténés.

## Resolution

Chall assez simple

On voit que dans le fichier on a: 2 strings retrouver
On voit dans le fichier 

<img width="524" height="318" alt="image" src="https://github.com/user-attachments/assets/f30eca7a-8eab-41a9-bc1e-185bd28dad2c" />

On voit par $1$ qu'on a du MD5

On met les hashs dans un fichier hash.txt a part
Puis on part en brut-force avec hashcat et une wordlist comme rockyou

<img width="433" height="157" alt="image" src="https://github.com/user-attachments/assets/c6fd6125-5169-4d9b-8e97-b5bd8a312e49" />




<img width="404" height="34" alt="image" src="https://github.com/user-attachments/assets/6a47b072-e26e-49fb-9fa4-9c79d68a61b1" />





<img width="386" height="67" alt="image" src="https://github.com/user-attachments/assets/3fef1e65-c5dd-49cb-b011-a1c40a46f4e8" />













