
# Write-Up — Kerberos Authentification Challenge

## 0. Introduction
Ce challenge consiste à analyser une capture réseau Kerberos [...]

## 1. Qu’est-ce que Kerberos ?
Kerberos est le protocole d’authentification d’Active Directory [...]

## 2. Flux AS-REQ / AS-REP
Description du flux [...]

## 3. PA-ENC-TIMESTAMP
Explication du timestamp chiffré [...]

## 4. Extraction du hash
Format Hashcat [...]

## 5. Cracking
Mot de passe trouvé : `kittycat12`

## 6. Flag final
```
RM{william.dupond@catcorp.local:kittycat12}
```
