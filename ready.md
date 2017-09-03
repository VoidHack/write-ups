We need to solve equation like <br/>
![equation](http://latex.codecogs.com/gif.latex?%5Cinline%202%5E%7Bm%20%5Coplus%20s%7D%5Cmod%20p%20%3D%20X)
<br />
where:<br />
__p__ is big prime number; <br/>
__m__ is our flag in bits; <br/>
__s__ is our input <br/>
__X__ is out output. <br/><br/>
We can only try to guess the bits of flag using XOR one by one from the end.<br />

First step is XORing with __0__ and __1__: <br/>
![equation](http://latex.codecogs.com/gif.latex?%5Cinline%202%5E%7Bm%20%5Coplus%20s_%7B0%7D%7D&plus;k_%7B0%7D*p%20%3D%20X_%7B0%7D)<br/>
![equation](http://latex.codecogs.com/gif.latex?%5Cinline%202%5E%7Bm%20%5Coplus%20s_%7B1%7D%7D&plus;k_%7B1%7D*p%20%3D%20X_%7B1%7D) <br/><br/>

![equation](http://latex.codecogs.com/gif.latex?%5Cinline%20m%20%5Coplus%20s_%7B0%7D) and 
![equation](http://latex.codecogs.com/gif.latex?%5Cinline%20m%20%5Coplus%20s_%7B1%7D) differ only in last bit. <br/>
If the last bit of __m__ is __0__, than ![equation](http://latex.codecogs.com/gif.latex?%5Cinline%20m%20%5Coplus%20s_%7B0%7D) = 1 + ![equation](http://latex.codecogs.com/gif.latex?%5Cinline%20m%20%5Coplus%20s_%7B1%7D), otherwise, 1 + ![equation](http://latex.codecogs.com/gif.latex?%5Cinline%20m%20%5Coplus%20s_%7B0%7D) = ![equation](http://latex.codecogs.com/gif.latex?%5Cinline%20m%20%5Coplus%20s_%7B1%7D) => <br/>
 => ![equation](http://latex.codecogs.com/gif.latex?%5Cinline%202%5E%7Bm%20%5Coplus%20s_%7B0%7D%7D) = ![equation](http://latex.codecogs.com/gif.latex?%5Cinline%202%20*%202%5E%7Bm%20%5Coplus%20s_%7B1%7D%7D) (__m__'s last bit is __0__) or ![equation](http://latex.codecogs.com/gif.latex?%5Cinline%202%5E%7Bm%20%5Coplus%20s_%7B1%7D%7D) = ![equation](http://latex.codecogs.com/gif.latex?%5Cinline%202%20*%202%5E%7Bm%20%5Coplus%20s_%7B0%7D%7D) (__m__'s last bit is __1__) <br/><br/>
__0__)
![equation](http://latex.codecogs.com/gif.latex?%5Cinline%20X_%7B0%7D-k_%7B0%7D*p%20%3D%202%20*%20%28X_%7B1%7D-k_%7B1%7D*p%29) => ![equation](http://latex.codecogs.com/gif.latex?%5Cinline%20k_%7B0%7D-%202*k_%7B1%7D%3D%20%5Cfrac%7BX_%7B0%7D%20-%20X_%7B1%7D%7D%7Bp%7D) <br/>
__1__)
![equation](http://latex.codecogs.com/gif.latex?%5Cinline%20X_%7B1%7D-k_%7B1%7D*p%20%3D%202%20*%20%28X_%7B0%7D-k_%7B0%7D*p%29) => ![equation](http://latex.codecogs.com/gif.latex?%5Cinline%20k_%7B1%7D-%202*k_%7B0%7D%3D%20%5Cfrac%7BX_%7B1%7D%20-%20X_%7B0%7D%7D%7Bp%7D) <br/><br/>

Left parts are natural. It means, left are natural too. Now we will find natural variant (__0__ or __1__) and save result. <br/><br/>
Second step is to undestand, how to find other bites. Now we will XOR with __1(i-1 random bits)__ and __0(same i-1 random bits)__ to became results, which degrees differ only in i position and one result is ![equation](http://latex.codecogs.com/gif.latex?%5Cinline%202%5E%7B2%5E%7Bi-1%7D%7D) times larger. <br/><br/>
It takes a lot of memory and time to calculate multiplier. We optimize it with modulus multiply. <br/><br/>

Our code to solve:
```py
#!/usr/bin/env python3
from socket import socket

p = 160634950613302858781995506902938412625377360249559915379491492274326359260806831823821711441204122060415286351711411013883400510041411782176467940678464161205204391247137689678794367049197824119717278923753940984084059450704378828123780678883777306239500480793044460796256306557893061457956479624163771194201
E = 10e-8

def calc(mul, x1, x2):
	return abs((x1 - (mul * x2)%p) % p) < E , abs((x2 - (mul * x1)%p) % p) < E

res = ''
for i in range(260*16):
	mul = 2 if i == 0 else (mul**2 % p)
	a,b = map(lambda x: hex(int(x, 2))[2:].encode()+b'\r\n',('1'+res, '0'+res))

	with socket() as s:
		s.connect(('ppc2.chal.ctf.westerns.tokyo', 28459))
		s.send(a)
		a = s.recv(2048).strip()[2:].decode()
		s.send(b)
		b = s.recv(2048).strip()[2:].decode()

	a,b = map(lambda x:int(x, 16), (a,b))

	v1, v2 = calc(mul, a, b)
	if v1 and v2:
		print('WRONG!')
		print(res)
		print(v1, v2)
		exit()
	res = ('1' if not v1 else '0') + res
	print('res:', res)
```
