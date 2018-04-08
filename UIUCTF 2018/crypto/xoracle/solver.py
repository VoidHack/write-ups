from base64 import b64decode
from socket import socket
from string import printable


ADDR = 'challenges1.uiuc.tf', 6464
printable = printable.encode()
KEY_LEN = 128

def get_msg():
    while True:
        with socket() as s:
            s.connect(ADDR)
            msg = b64decode(s.recv(2<<10))
        if len(msg) == 1536:
            return msg

def xor_bytetrings(a, b):
    return bytes((x^y for x,y in zip(a,b)))

def find_msgs():
    msgs ={get_msg()}
    needed = set(range(128))

    while needed:
        print(len(msgs), needed)
        new_msg = get_msg()
        for msg in list(msgs):
            key = xor_bytetrings(new_msg, msg)
            good_part, last_part = key[:KEY_LEN], key[KEY_LEN:]

            if good_part in last_part:
                i = last_part.index(good_part)
                print('\t', i)
                if i in needed:
                    yield (i, new_msg)
                    needed -= {i}
                    msgs -= {msg}
                    continue
        msgs.add(new_msg)

if __name__ == "__main__":
    for i, text in find_msgs():
        with open('l_{}'.format(i), 'wb') as f:
            f.write(text)

    res = [0]
    with open('l_0', 'rb') as f: 
        original = f.read()
    
    for i in range(1,128):
        with open('l_{}'.format(i), 'rb') as f: 
            shifted = f.read()
        
        or_blocks = [original[KEY_LEN*x:KEY_LEN*(x+1)] for x in range(0,2)]
        sh_blocks = [shifted[(KEY_LEN+i)*x:(KEY_LEN+i)*(x+1)] for x in range(0,2)]

        H1 = xor_bytetrings(*or_blocks)
        H2 = xor_bytetrings(*sh_blocks)

        res.append(H1[i] ^ H2[0])

    i = 80
    msg_first = [i^x for x in res]
    # print(bytes(msg_first))
    key = xor_bytetrings(msg_first, original)
    res = xor_bytetrings(key*13, original)
    with open('res.zip', 'wb') as f:
        f.write(res)