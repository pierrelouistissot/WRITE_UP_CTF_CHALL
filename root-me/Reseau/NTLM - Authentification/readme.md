## Contexte:

Énoncé
Vous êtes mandaté par l’équipe SOC de l’entreprise Cat Corporation pour retrouver le mot de passe d’un utilisateur lié à une connexion NTLM over SMB suspecte.

Format du flag : RM{userPrincipalName:password}


Le protocole d'authentification NTLM ou “New Technology Lan Manager” a été créé en 1993 pour remplacer le protocole Lan Manager devenu trop vulnérable. NTLM est utilisé pour vérifier l'identité d'un utilisateur ou d'une machine sur un réseau en se basant sur un système de challenge-response.

Le principe de l’authentification NTLM est le suivant :

En premier lieu, le client indique au serveur qu’il souhaite s’authentifier.

Puis, le serveur répond avec un défi, ou un challenge, qui n’est rien d’autre qu’une suite aléatoire de caractères.

Ensuite, le client chiffre ce challenge avec son secret (hash NT de son mot de passe ou hash LM pour rétrocompatibilité), et renvoie le résultat au serveur, c’est sa réponse.

Enfin, le serveur effectue la même opération avec le hash du mot de passe correspondant au nom de domaine et au nom d’utilisateur voulant s’authentifier. Il compare ensuite le résultat avec celui envoyé par le client. Si la comparaison est valide, le client est authentifié sur le serveur.

