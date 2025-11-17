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

** kali@DESKTOP-N0M80R7:~/volatility3$ python3 vol.py -f ~/memory.dmp windows.pstree **

<img width="831" height="836" alt="image" src="https://github.com/user-attachments/assets/8d65dcdc-838a-4b99-a4f3-588a1d3fc199" />







