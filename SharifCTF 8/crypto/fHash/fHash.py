from hashlib import md5


def foo(h, m):
    return md5(h.encode('utf-8') + m.encode('utf-8')).hexdigest()[:4]


def round(hl, m, hr):
    return foo(hl, m), foo(hr, m)


def fHash(hl, hr, M):
    message = list(map(''.join, zip(*[iter(M)] * 4)))
    for m in message:
        hl, hr = round(hl, m, hr)
    return hl + hr


if __name__ == '__main__':
    print(fHash('7575', 'A8A8', '7368617269666374'))