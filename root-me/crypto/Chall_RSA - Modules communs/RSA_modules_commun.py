
import base64
from cryptography.hazmat.primitives import serialization

with open("key1_pub.pem", "rb") as f:
    pub1 = serialization.load_pem_public_key(f.read())
with open("key2_pub.pem", "rb") as f:
    pub2 = serialization.load_pem_public_key(f.read())

n  = pub1.public_numbers().n
e1 = pub1.public_numbers().e
e2 = pub2.public_numbers().e


c1 = int.from_bytes(base64.b64decode(open("message1","rb").read()), "big")
c2 = int.from_bytes(base64.b64decode(open("message2","rb").read()), "big")


def egcd(a, b):
    if b == 0:
        return (1, 0, a)
    x, y, g = egcd(b, a % b)
    return (y, x - (a // b) * y, g)

a, b, g = egcd(e1, e2)
assert g == 1
print(f"Coeffs: a = {a}, b = {b}")

def modinv(x, n):
    return pow(x, -1, n)

if a >= 0:
    part1 = pow(c1, a, n)
else:
    part1 = pow(modinv(c1, n), -a, n)

if b >= 0:
    part2 = pow(c2, b, n)
else:
    part2 = pow(modinv(c2, n), -b, n)

m = (part1 * part2) % n


m_bytes = m.to_bytes((m.bit_length() + 7) // 8, "big")
msg = m_bytes.decode()
print("Message:")
print(msg)
