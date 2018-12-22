from Crypto.Util.number import isPrime
from random import getrandbits

def genKey(k):

	while True:
		r=getrandbits(k)
		while(r%2):
			r=getrandbits(k)
	
		p =  3 * r**2 +  2 * r + 7331
		q = 17 * r**2 + 18 * r + 1339
		n = p * q

		if(isPrime(p) and isPrime(q)):
			return (p,q) , n

def encrypt(m,pubkey):

	c=m**2 % pubkey
	return c

privkey,pubkey = genKey(256)

flag = open('flag.txt').read().strip()
while(len(flag)<125):
	flag+='X'
flag = int(flag.encode('hex'),16)

ct=encrypt(flag,pubkey)

with open('flag.enc','w') as f:
	f.write('ct = ' + str(ct))

with open('pubkey.txt','w') as f:
	f.write('pubkey = ' + str(pubkey))

with open('privkey.txt','w') as f:
	f.write('privkey = ' + str(privkey))
