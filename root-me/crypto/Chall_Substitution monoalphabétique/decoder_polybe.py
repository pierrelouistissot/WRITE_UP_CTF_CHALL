
#Decoder le polybe

polybe = {
    'a': ['a','b','c','d','e'],
    'b': ['f','g','h','i','j'],
    'c': ['k','l','m','n','o'],
    'd': ['p','q','r','s','t'],
    'e': ['u','v','x','y','z']
}

with open("ch12.txt", "r", encoding="utf-8") as f:
    data = f.read().strip()

decoded = []
for token in data.split():
    word = []
    for i in range(0, len(token), 2):
        row = token[i]              # lettre (a–e)
        col = int(token[i+1]) - 1   # chiffre (1–5)
        word.append(polybe[row][col])
    decoded.append(''.join(word))

plain_text = ' '.join(decoded)
print(plain_text)
