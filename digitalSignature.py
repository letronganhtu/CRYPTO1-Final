import random
import hashlib

def fast_pow_mod(a, b, p):
    res = 1
    while b:
        if b % 2 == 1:
            res = (res * a) % p
        a = (a * a) % p
        b = b // 2
    return res

def miller_rabin(n, k):

    if n == 2 or n == 3:
        return True

    if n % 2 == 0:
        return False

    r, s = 0, n - 1
    while s % 2 == 0:
        r += 1
        s //= 2
    for _ in range(k):
        a = random.randrange(2, n - 1)
        x = fast_pow_mod(a, s, n)
        if x == 1 or x == n - 1:
            continue
        for _ in range(r - 1):
            x = fast_pow_mod(x, 2, n)
            if x == n - 1:
                break
        else:
            return False
    return True

def findInverse(x, y):
    return pow(x, -1, y)

def primeGen(length = 512):
    n = random.getrandbits(length)
    n = n | 1
    while not miller_rabin(n, 20):
        n += 2
    return n

def genRSA(keyLength=512):
    p = primeGen(keyLength)
    q = primeGen(keyLength)
    n = p * q
    phi = (p - 1) * (q - 1)
    e = 65537
    d = findInverse(e, phi)

    return e, d, n

def RSAsign(doc, d, n):
    hdoc = hashlib.sha256(doc.encode())
    id = int.from_bytes(hdoc.digest(), 'big')
    s = fast_pow_mod(id, d, n)
    return s

def RSAverify(doc, s, e, n):
    hdoc = hashlib.sha256(doc.encode())
    id = int.from_bytes(hdoc.digest(), 'big')
    idrep = fast_pow_mod(s, e, n)
    
    return id == idrep
