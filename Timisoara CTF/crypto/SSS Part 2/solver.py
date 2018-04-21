from string import ascii_letters
from Crypto.Util.number import long_to_bytes, bytes_to_long

parts = [
    7714685804569579757659784, 
    7534756766114272409848924, 
    7685963206231043158730376, 
    7164946524794170391755686
]

flag = b'timctf{'

if __name__ == "__main__":
    # for x in range(0x100): # for each of 3 last bytes
    x = flag + b'd0_'
    i = parts[0] - bytes_to_long(x)
    res = b''.join(long_to_bytes(y - i) for y in parts)
    print(res)