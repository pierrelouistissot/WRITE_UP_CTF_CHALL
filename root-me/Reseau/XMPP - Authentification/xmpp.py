import base64
import hashlib
import hmac
import itertools

# ====== Données récupérées dans la capture (via base64 des CDATA) ======

client_first_full = "n,,n=koma_test,r=hydra"
client_first_bare = "n=koma_test,r=hydra"  # on enlève le "n,,"
server_first = "r=hydraFe3A1scL7C0jtKsm+kcg96MWg769FuRu,s=kM6lTjjnZW4F8WLboyagcA==,i=4096"
server_final = "v=YQlegvbEwDo2o60YiK2iAkYyPKE="  # valeur qu'on veut retrouver

# Parse server_first
parts = dict(p.split("=", 1) for p in server_first.split(","))
nonce = parts["r"]                       # hydraFe3A1...
salt_b64 = parts["s"]                    # kM6lTjjnZW4F8WLboyagcA==
iterations = int(parts["i"])             # 4096

expected_server_sig_b64 = server_final.split("=", 1)[1]

salt = base64.b64decode(salt_b64)

def compute_server_final(password: str) -> str:
    """
    Rejoue la partie serveur de SCRAM-SHA-1 pour un mot de passe donné
    et renvoie la chaîne 'v=.....' comme dans le paquet SUCCESS.
    """
    # SaltedPassword = PBKDF2-SHA1(password, salt, iterations)
    salted_password = hashlib.pbkdf2_hmac("sha1", password.encode(), salt, iterations)

    # ServerKey = HMAC(SaltedPassword, "Server Key")
    server_key = hmac.new(salted_password, b"Server Key", hashlib.sha1).digest()

    # clientFinalMessageBare = "c=biws,r=" + nonce
    client_final_bare = f"c=biws,r={nonce}"

    # authMessage = client-first-bare + "," + server-first + "," + client-final-bare
    auth_message = ",".join([client_first_bare, server_first, client_final_bare])

    # ServerSignature = HMAC(ServerKey, authMessage)
    server_signature = hmac.new(server_key, auth_message.encode(), hashlib.sha1).digest()

    return "v=" + base64.b64encode(server_signature).decode()


# ====== Bruteforce ======

charset = "_abcdefghijklmnopqrstuvwxyz"  # caractère après 'koma'
max_extra_len = 2                        # longueur max de suffixe

def bruteforce():
    for length in range(1, max_extra_len + 1):
        print(f"Test des mots de passe de type 'koma' + {length} char(s)")
        for tup in itertools.permutations(charset, length):
            pwd = "koma" + "".join(tup)
            v = compute_server_final(pwd)
            if v == server_final:
                print("Mot de passe trouvé")
                print("mdp :", pwd)
                sha1 = hashlib.sha1(pwd.encode()).hexdigest()
                print("SHA1     :", sha1)
                return
    print("Rien trouvé dans cet espace de recherche :(")

if __name__ == "__main__":
    bruteforce()
