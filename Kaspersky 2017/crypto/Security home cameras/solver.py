with open('secret_encrypted.png', 'rb') as f: data = f.read()
with open('res.png','wb') as f: f.write(bytes(map(lambda x: x^255, data)))