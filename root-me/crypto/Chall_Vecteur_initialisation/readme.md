## Contexte

Le vecteur d’initialisation a été perdu, il ne vous reste malheureusement qu’un texte chiffré. A vous de retrouver le vecteur perdu en utilisant ces informations. Le texte a été chiffré en AES-256 CBC, et le padding utilisé est le standard PKCS#7.

Le mot de passe de validation est le vecteur initial (en ASCII).

### Texte clair :

Marvin: "I am at a rough estimate thirty billion times more intelligent than you. Let me give you an example. Think of a number, any number."
Zem: "Er, five."
Marvin: "Wrong. You see?"

### Texte chiffré :

cY1Y1VPXbhUqzYLIOVR0RhUXD5l+dmymBfr1vIKlyqD8KqHUUp2I3dhFXgASdGWzRhOdTj8WWFTJ
PK0k/GDEVUBDCk1MiB8rCmTZluVHImczlOXEwJSUEgwDHA6AbiCwyAU58e9j9QbN+HwEm1TPKHQ6
JrIOpdFWoYjS+cUCZfo/85Lqi26Gj7JJxCDF8PrBp/EtHLmmTmaAVWS0ID2cJpdmNDl54N7tg5TF
TrdtcIplc1tDvoCLFPEomNa5booC


###Clé :

AQIDBAUGBwgJCgsMDQ4PEBESExQVFhcYGRqrHB0eHyA=

## Analyse

En AES-CBC:

<img width="361" height="122" alt="image" src="https://github.com/user-attachments/assets/b8493ddf-9ff0-4769-a9bb-0f9060583176" />


Donc pour trouver le IV on va juste bosser sur le premier block, donc on peu appliquer simplement un AES en mode ECB


Le code est simple a comprendre
