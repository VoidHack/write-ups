#!/usr/bin/python3
from Crypto.PublicKey import RSA
from Crypto.Util.number import *

FLAG = open('flag.txt', 'r').read().strip()

def menu():
    print()
    print('[1] Encrypt')
    print('[2] Decrypt')
    print('[3] Exit')
    return input()


def encrypt(m):
    return pow(m, rsa.e, rsa.n)


def decrypt(c):
    return pow(c, rsa.d, rsa.n)


rsa = RSA.generate(1024)
flag_encrypted = pow(bytes_to_long(FLAG.encode()), rsa.e, rsa.n)
used = [bytes_to_long(FLAG.encode())]

print('Ho, ho, ho and welcome back!')
print('Your list for this year:\n')
print('Sarah - Nice')
print('Bob - Nice')
print('Eve - Naughty')
print('Galf - ' + hex(flag_encrypted)[2:])
print('Alice - Nice')
print('Johnny - Naughty')

for i in range(5):
    choice = menu()

    if choice == '1':
        m = bytes_to_long(input('\nPlaintext > ').strip().encode())
        used.append(m)

        print('\nEncrypted: ' + str(encrypt(m)))

    elif choice == '2':
        c = int(input('\nCiphertext > ').strip())

        if c == flag_encrypted:
            print('Ho, ho, no...')

        else:
            m = decrypt(c)
            
            for no in used:
                if m % no == 0:
                    print('Ho, ho, no...')
                    break
                
            else:
                print('\nDecrypted: ' + str(m))

    elif choice == '3':
        print('Till next time.\nMerry Christmas!')
        break

print('Too many requests made... Disconnecting...')
