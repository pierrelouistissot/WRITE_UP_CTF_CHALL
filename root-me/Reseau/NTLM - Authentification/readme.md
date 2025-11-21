## Contexte:

Entreprise fictive : Cat Corporation

Équipe : SOC qui enquête sur une authentification NTLM over SMB suspecte.

Fichier fourni : ntlm_auth.pcapng (capture réseau, hash SHA256 donné dans l’énoncé pour vérifier l’intégrité).

Objectif : retrouver le mot de passe de l’utilisateur utilisé dans cette authentification NTLM.

Format du flag :

RM{userPrincipalName:password}


## fonctionnement de NTLM

### Le handshake

**Type 1 – NEGOTIATE :**
Le client envoie un message au serveur pour annoncer qu’il souhaite utiliser NTLM, avec ses capacités.

**Type 2 – CHALLENGE :**
Le serveur répond avec :

Un server challenge (8 octets aléatoires).

Des infos sur le domaine/serveur cible.

**Type 3 – AUTHENTICATE :**
Le client renvoie :

Le nom d’utilisateur (ici john.doe).

Le domaine (ici catcorp.local).

Le type de réponse NTLM (NTLMv1 ou NTLMv2 ; ici NTLMv2).

Un NTLMv2 Response calculé à partir :

du mot de passe,

du challenge serveur,

et d’un blob contenant des infos (timestamp, target info, etc.).

### NTLMv2

Pour NTLMv2 :

On calcule d’abord le NTLM hash : MD4 du mot de passe en UTF-16LE.

Puis le NTLMv2 hash = HMAC-MD5(NTLM_hash, (USERNAME_UPPER + DOMAIN) en UTF-16LE).

Enfin la NTProofStr = HMAC-MD5(NTLMv2_hash, ServerChallenge + Blob).

Le serveur, qui connaît le NTLM hash (stocké en AD), refait le calcul et vérifie que la NTProofStr correspond.

## analyse

On a ensuite repéré la trame 51 :

SMB2 - Session Setup Request (NTLMSSP_AUTH) avec :

User name : john.doe

Domain name : catcorp.local

NTLMv2 Response détaillée

Dans la partie NTLMSSP_AUTH de cette trame, Wireshark te donne notamment :

Server Challenge : trouvé dans la trame Type 2 (CHALLENGE), ici :
1944952f5b845d73

NTProofStr (début du NTLMv2 Response) :
5c336c6b69fd2cf7b64eb0bde3102162

NTLMv2 Response blob (le reste après la NTProofStr) :
01010000000000001a9790044b63da0175...0000000000000000

À partir des infos de la trame 51, on construit la ligne au format attendu par hashcat (mode 5600, NetNTLMv2).

USERNAME::DOMAIN:SERVER_CHALLENGE:NT_PROOF:NTLM_RESPONSE_BLOB

```
JOHN.DOE::catcorp.local:1944952f5b845db1:5c336c6b69fd2cf7b64eb0bde3102162:01010000000000001a9790044b63da0175304c546c6f34320000000002000e0043004100540043004f005200500001000800440043003000310004001a0063006100740063006f00720070002e006c006f00630061006c000300240044004300300031002e0063006100740063006f00720070002e006c006f00630061006c0005001a0063006100740063006f00720070002e006c006f00630061006c00070008001a9790044b63da010900120063006900660073002f0044004300300031000000000000000000


```

Puis on crack tout ca avec hashcat en mode -m 5600 => NetNTLMv2

```
hashcat -m 5600 hash.txt rockyou.txt -O

```
