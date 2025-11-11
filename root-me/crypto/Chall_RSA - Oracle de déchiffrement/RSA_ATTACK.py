import socket
import re

# Paramètres du challenge
n = 456378902858290907415273676326459758501863587455889046415299414290812776158851091008643992243505529957417209835882169153356466939122622249355759661863573516345589069208441886191855002128064647429111920432377907516007825359999
e = 65537
c = 41662410494900335978865720133929900027297481493143223026704112339997247425350599249812554512606167456298217619549359408254657263874918458518753744624966096201608819511858664268685529336163181156329400702800322067190861310616

HOST = "challenge01.root-me.org"
PORT = 51031

#On choisit s = 2 et on calcule c' = c * s^e mod n
s = 2
c_prime = (c * pow(s, e, n)) % n


with socket.create_connection((HOST, PORT)) as sock:
    # Lire la bannière/prompt
    banner = sock.recv(4096).decode()
    print("Banner du serveur :")
    print(banner)

    # Envoyer c' en décimal
    sock.sendall(str(c_prime).encode() + b"\n")

    # Lire la réponse (plaintext correspondant à c')
    resp = sock.recv(4096).decode()
    print("[*] Réponse brute :")
    print(resp)

#Extraire l'entier p depuis la réponse
#    (la ligne contient "The corresponding plaintext is: <p>")
match = re.search(r"(\d+)", resp)
if not match:
    print("Impossible de trouver l'entier dans la réponse.")
    exit(1)

p = int(match.group(1))
print("p =", p)

#Calculer m = p * s^{-1} mod n
inv_s = pow(s, -1, n)       # inverse de 2 modulo n
m = (p * inv_s) % n
print("[+] m (int) =", m)

#Convertir m en bytes puis en texte
m_bytes = m.to_bytes((m.bit_length() + 7) // 8, "big")
print("[+] m (bytes) =", m_bytes)

try:
    m_text = m_bytes.decode("utf-8")
    print("[+] m (utf-8) =", m_text)
except UnicodeDecodeError:
    print("[-] Impossible de décoder en utf-8.")
    exit(1)

