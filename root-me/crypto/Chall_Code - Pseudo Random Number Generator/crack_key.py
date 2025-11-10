# Le script balaie toutes les secondes de décembre 2012 (UTC) par défaut.
# Il vérifie si le fichier déchiffré commence par 'BZh' (signature d'un .bz2).


import sys
import os
from datetime import datetime, timezone, timedelta


def rand_gen(seed):
    holdrand = seed & 0xffffffff
    while True:
        holdrand = (holdrand * 214013 + 2531011) & 0xffffffff
        yield (holdrand >> 16) & 0x7fff

CHARSET = (
    "abcdefghijklmnopqrstuvwxyz"
    "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    "123456789"
)
KEY_SIZE = 32

def generate_key_from_seed(seed):
    g = rand_gen(seed)
    key_chars = []
    for _ in range(KEY_SIZE):
        r = next(g)
        key_chars.append(CHARSET[r % (len(CHARSET))])
    return ''.join(key_chars)

def try_decrypt_with_key_first_bytes(enc_bytes, key, nb=16):
    out = bytearray()
    j = 0
    klen = len(key)
    for i in range(min(nb, len(enc_bytes))):
        out.append(enc_bytes[i] ^ ord(key[j]))
        j += 1
        if j >= klen:
            j = 0
    return bytes(out)

def decrypt_all(enc_bytes, key):
    out = bytearray(len(enc_bytes))
    j = 0
    klen = len(key)
    for i in range(len(enc_bytes)):
        out[i] = enc_bytes[i] ^ ord(key[j])
        j += 1
        if j >= klen:
            j = 0
    return bytes(out)

def main():
    if len(sys.argv) != 2:
        return

    enc_path = sys.argv[1]
    if not os.path.isfile(enc_path):
        print("Fichier introuvable:", enc_path)
        return

    with open(enc_path, "rb") as f:
        enc = f.read()

    # On prend UTC par défaut : 2012-12-01 00:00:00 -> 2012-12-31 23:59:59
    start = datetime(2012, 12, 1, 0, 0, 0, tzinfo=timezone.utc)
    end   = datetime(2012, 12, 31, 23, 59, 59, tzinfo=timezone.utc)

    start_ts = int(start.timestamp())
    end_ts = int(end.timestamp())

    target = b'BZh'
    tried = 0

    for seed in range(start_ts, end_ts+1):
        tried += 1
        key = generate_key_from_seed(seed)
        first = try_decrypt_with_key_first_bytes(enc, key, nb=8)
        if first.startswith(target):
            print()
            print("Possible seed trouvée")
            print("    seed (time_t) :", seed, "->", datetime.fromtimestamp(seed, tz=timezone.utc).isoformat())
            print("    key :", key)
            dec = decrypt_all(enc, key)
            outpath = enc_path + ".dec"
            with open(outpath, "wb") as out:
                out.write(dec)
            print("    Fichier déchiffré écrit :", outpath)
            return
    print("Aucune seed trouvée dans l'intervalle testé.")

if __name__ == "__main__":
    main()
