# __Kaspersky Industrial CTF Quals 2017.__ 
## _Security home cameras_

## Information
**Category:** Crypto
**Points:** 300
**Description:** 
> The smart home system has the function of remote monitoring of what is happening in the home and every few minutes sends pictures of the surveillance cameras to the owner of the house. You successfully intercepted the network traffic of this system, however, its creators took care of the security of their users data and encrypted the pictures. Decrypt the provided image and you will find the flag.
[secret_encrypted.png](https://ctf.kaspersky.com/contests/1/files/8/)

## Solution
Let's see at the PNG header. If we xor the header of this [picture](secret_encrypted.png) with it, we get only 255 bytes. 
Let's try to [xor](solver.py) whole picture with this byte. Answer is here!
<p>
    <img src="konata.jpg">
</p>