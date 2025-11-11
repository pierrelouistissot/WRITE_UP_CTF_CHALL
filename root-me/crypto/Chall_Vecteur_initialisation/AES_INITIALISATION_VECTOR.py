from Crypto.Cipher import AES
import base64

Plain='Marvin: "I am at'
print(len(Plain))
Key=base64.b64decode('AQIDBAUGBwgJCgsMDQ4PEBESExQVFhcYGRqrHB0eHyA=')
Cipher=base64.b64decode('cY1Y1VPXbhUqzYLIOVR0RhUXD5l+dmymBfr1vIKlyqD8KqHUUp2I3dhFXgASdGWzRhOdTj8WWFTJPK0k/GDEVUBDCk1MiB8rCmTZluVHImczlOXEwJSUEgwDHA6AbiCwyAU58e9j9QbN+HwEm1TPKHQ6JrIOpdFWoYjS+cUCZfo/85Lqi26Gj7JJxCDF8PrBp/EtHLmmTmaAVWS0ID2cJpdmNDl54N7tg5TFTrdtcIplc1tDvoCLFPEomNa5booC')
objet=AES.new(Key,AES.MODE_ECB)
VI=objet.decrypt(Cipher)
for i in range(len(Plain)):
  print(chr(VI[i]^ord(Plain[i])),end='')