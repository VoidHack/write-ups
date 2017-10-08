import re
import requests
from base64 import b64encode, b64decode


def main():
    ciphertext = 'oWTWItwxAFINQBrozTSNqW2q4HucO6nFjT+SSFMt4mO94Dm4M+dxMSktiRv+88tVt827KTLQrbu6v2Vmki9OSw=='
    decoded_ciphertext = b64decode(ciphertext)
    plain = '{"name": "a", "show_flag": false}'
    plain_des = '{"name": "a", "show_flag": true }'
    for i in range(0, 16):
        by = bytes([ord(plain[i + 16]) ^ decoded_ciphertext[i + 16] ^ ord(plain_des[i + 16])])
        print(plain_des[i + 16], plain[i + 16])
        decoded_ciphertext = decoded_ciphertext[:i + 16] + by + decoded_ciphertext[i + 1 + 16:]
    reg = re.compile(r"can't decode byte (.+?) in position (.+?):")
    for pos in range(0, 16):
        print(pos)
        for i in range(0, 256):
            data = decoded_ciphertext[:pos] + bytes(bytearray([i])) + decoded_ciphertext[pos + 1:]
            val = make_request(b64encode(data).decode(), reg, pos)
            if val:
                val = int(val, 16)
                res = bytes([(val ^ i) ^ ord(plain[pos])])
                decoded_ciphertext = decoded_ciphertext[:pos] + res + decoded_ciphertext[pos + 1:]
                break
            print(i)
    print(decoded_ciphertext)


def make_request(cookie, reg, position):
    url = 'http://95.85.51.183/'
    headers = {"Cookie": f'user_info={cookie}'}
    r = requests.get(url, headers=headers)
    print(cookie)
    print(r.text[-100:])
    match = re.findall(reg, r.text)
    if match and match[0][1] == str(position):
        return match[0][0]


if __name__ == '__main__':
    main()
