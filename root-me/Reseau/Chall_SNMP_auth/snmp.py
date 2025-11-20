import sys
import hashlib

# Message SNMPv3 entier (Frame 3) - en hex
MSG_HEX = (
    "3081800201033011020420dd06a7020300ffe3040105020103043130"
    "2f041180001f8880e9bd0c1d12667a51000000000201050201200404"
    "75736572040cb92621f4a93d1bf9738cd5bd04003035041180001f88"
    "80e9bd0c1d12667a51000000000400a11e02046b4c5ac20201000201"
    "003010300e060a2b06010201041e0105010500"
)

# Valeur du champ msgAuthenticationParameters qu'on veut retrouver
AUTH_HEX = "b92621f4a93d1bf9738cd5bd"

# EngineID de l'agent SNMP, extrait de la trame
ENGINEID_HEX = "80001f8880e9bd0c1d12667a5100000000"


def compute_snmpv3_md5(password: str) -> str:
    """
    Implémente l'auth SNMPv3 MD5 , version simplifiée :
      - password -> Ku (MD5 sur 1 Mo du mot de passe répété)
      - Ku + engineID + Ku -> Kul
      - HMAC-MD5(Kul, message_avec_auth_à_0) -> 12 octets (96 bits)
    Retourne le digest (12 octets) en hex.
    """
    pw_bytes = password.encode("utf-8")
    if not pw_bytes:
        return ""

    # 1) Password -> Ku (1 Mo de password répété)
    one_mb = 1048576
    repeat_count = one_mb // len(pw_bytes) + 1
    buf = (pw_bytes * repeat_count)[:one_mb]
    ku = hashlib.md5(buf).digest()

    # 2) Localisation avec l'EngineID -> Kul
    engineid = bytes.fromhex(ENGINEID_HEX)
    kul = hashlib.md5(ku + engineid + ku).digest()

    # 3) HMAC-MD5-96 sur le message avec auth field à 0
    msg_zeroed_hex = MSG_HEX.replace(AUTH_HEX, "0" * len(AUTH_HEX))
    msg_zeroed = bytes.fromhex(msg_zeroed_hex)

    block_size = 64
    if len(kul) > block_size:
        key_block = hashlib.md5(kul).digest()
    else:
        key_block = kul.ljust(block_size, b"\x00")

    ipad = bytes([0x36]) * block_size
    opad = bytes([0x5C]) * block_size

    k_ipad = bytes(a ^ b for a, b in zip(key_block, ipad))
    k_opad = bytes(a ^ b for a, b in zip(key_block, opad))

    inner = hashlib.md5(k_ipad + msg_zeroed).digest()
    outer = hashlib.md5(k_opad + inner).digest()

    # SNMPv3 garde seulement les 12 premiers octets (96 bits)
    return outer[:12].hex()


def brute_force(dictionary_path: str) -> None:
    target = AUTH_HEX.lower()

    f = open(dictionary_path, encoding="utf-8", errors="ignore")

    with f:
        for i, line in enumerate(f, 1):
            password = line.strip()
            if not password:
                continue

            if i % 1000 == 0:
                print(f"{i} mots testés")

            digest = compute_snmpv3_md5(password)

            if digest == target:
                print(f"Mot de passe: {password}")
                return

    print("Mot de passe non trouvé.")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit(1)

    dict_path = sys.argv[1]
    brute_force(dict_path)
