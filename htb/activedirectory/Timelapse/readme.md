
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

On trouve ces logins la:

```
$p = ConvertTo-SecureString 'E3R$Q62^12p7PLlC%KWaxuaV' -AsPlainText -Force
$c = New-Object System.Management.Automation.PSCredential ('svc_deploy', $p)
```
C est les logs du compte `svc_deploy`

svc = Service Account
En environnement Windows/Active Directory, les comptes svc_* sont des comptes de service

des comptes créés non pas pour un humain mais pour faire tourner des applications/services.
Exemples courants :

svc_backup → compte qui fait les sauvegardes
svc_sql → compte qui fait tourner SQL Server
svc_deploy → compte qui fait les déploiements (push de code, scripts d'install...)

Ca nous rajoute donc un compte
On regarde les groupes et acces de svc_deploy

<img width="749" height="527" alt="image" src="https://github.com/user-attachments/assets/3ad22d46-3590-4fe5-8826-fc291601b0d4" />

LAPS (Local Administrator Password Solution) c'est un outil Microsoft qui génère automatiquement des mots de passe aléatoires pour le compte Administrator local de chaque machine du domaine, et les stocke dans l'Active Directory.

<img width="1369" height="271" alt="image" src="https://github.com/user-attachments/assets/79299d08-3065-4cac-aaf7-1ecb7ba7efeb" />

<img width="1369" height="344" alt="image" src="https://github.com/user-attachments/assets/583d92c3-6a67-4894-b93d-4f1e653851c2" />

ms-Mcs-AdmPwd c'est l'attribut AD où LAPS stocke le mot de passe Administrator. 

Le mot de passe Administrator de DC01 est :

`m6%04I]nG19[ymlb+V53%19b`

On se connecte en WinRM, et on trouve le mdp de l'admin: ca98ac546626da5fcd6df05d2e748e08





