# Table de substitution
substitution = {
    'a':'t','b':'j','c':'e','d':'o','e':'z','f':'r','g':'h','h':'c','i':'m',
    'j':'x','k':'q','l':'g','m':'b','n':'l','o':'v','p':'s','q':'i','r':'d',
    's':'n','t':'y','u':'p','v':'f','x':'a','z':'u'
}

with open("polybe_decoded.txt", "r", encoding="utf-8") as f:
    data = f.read()

decoded = ''.join(substitution.get(c, c) for c in data)

print(decoded)
