
<img width="801" height="351" alt="image" src="https://github.com/user-attachments/assets/e107f3b8-eb2e-44f5-9bb4-2fef4eae8602" />


<img width="804" height="377" alt="image" src="https://github.com/user-attachments/assets/5dd2ddf4-ad72-4d1d-9997-753cbef0cfcc" />

<img width="785" height="150" alt="image" src="https://github.com/user-attachments/assets/4a6b3ada-684f-4602-b869-2a4272426224" />

MDP:supremelegacy

On trouve un fichier .pfx

`Un fichier .pfx (PKCS#12) est un certificat SSL + clé privée regroupés dans un seul fichier protégé par mot de passe. Ici il appartient à l'utilisateur legacyy et va servir à s'authentifier sur WinRM à la place d'un mot de passe classique.`

<img width="785" height="150" alt="image" src="https://github.com/user-attachments/assets/c1045ad1-8b36-45b3-9419-cec9f8ae8d38" />

On a comme mdp: `thuglegacy`


Le fichier legacyy_dev_auth.pfx contient :

Un certificat → prouve l'identité de legacyy
Une clé privée → permet de signer/chiffrer

WinRM peut accepter une authentification par certificat à la place d'un mot de passe. Donc avec ce .pfx tu peux te connecter en tant que legacyy sans connaître son mot de passe.

On tente donc:

<img width="785" height="899" alt="image" src="https://github.com/user-attachments/assets/007c12f0-41e8-44b8-85d1-7cef225102e8" />

On trouve le premier flag:0ca974158184478c71c793d2966304ed

Maintenant classique, on peut cherche les droits que le pc legacy a:


on trouve ca dans l'historique powershell :

<img width="1594" height="231" alt="image" src="https://github.com/user-attachments/assets/927b127e-2612-4cd9-aee2-e423837ebfcc" />

