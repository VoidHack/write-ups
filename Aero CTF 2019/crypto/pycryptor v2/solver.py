import struct
from pycryptor_v2 import p_8, p_16, p_32, u_8, u_16, u_32
from pycryptor_v2 import Crc

hexdigits = "0123456789abcdef"
KEY = "ed40f1e93ab22ea7"
CRC = Crc()

def xor_bytes(a, b):
    return "".join([chr(ord(a[i]) ^ ord(b[i % len(b)])) for i in xrange(len(a))])

def calculate_crc(s):
    return CRC(s)

def read_file(filename):
    with open(filename, 'rb') as f:
        return f.read()

def generate_gammas():
    for x in range(0x80):
        for y in range(0x80):
            gamma = ''
            block_crc = [x, y]

            for i in range(16):
                val = block_crc[i % 2]
                val ^= ord(KEY[i]) 
                val &= 0xff
                gamma += chr(val)

            _x = x << 1
            _y = y << 1

            a = _x << 8 | _y
            b = _x << 8 | (_y | 1)
            c = (_x | 1) << 8 | _y
            d = (_x | 1) << 8 | (_y | 1)
            crcs = set(map(p_16, {a, b, c, d}))

            yield gamma, crcs

def decrypt_block_part(block, gammas):
    for gamma, gamma_crcs in gammas:
        decrypt_block = xor_bytes(block, gamma)
        real_block_crc = p_16(calculate_crc(decrypt_block))

        if real_block_crc in gamma_crcs:
            yield decrypt_block

def decrypt_block(block, crc, gammas):
    second_parts = list(decrypt_block_part(block[16:], gammas))

    for first_part in decrypt_block_part(block[:16], gammas):
        for second_part in second_parts:
            dec_block = first_part + second_part

            if CRC(dec_block) == crc:
                return dec_block

def decrypt_file(data):
    gammas = list(generate_gammas())
    print "{} gammas loaded".format(len(gammas))
    blocks = []
    i = 0

    while i < len(data):
        block = data[i:i+32]
        crc = u_16(data[i+32:i+34])

        blocks.append((block, crc))
        i += 34

    with open("res.jpg", 'wb') as fd:
        for i, (block, crt) in enumerate(blocks):
            print "{}/{}".format(i, len(blocks))
            dec_block = decrypt_block(block, crt, gammas)
            fd.write(dec_block)
            fd.flush()

if __name__ == "__main__":
    data = read_file("test_image.enc")
    decrypt_file(data)