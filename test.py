import random
import numpy as np

def fast_pow(a, b, p):
    res = 1
    while b:
        if b % 2 == 1:
            res = (res * a) % p
        a = (a * a) % p
        b = b // 2
    return res

with open('parameter.txt', encoding = 'utf-8') as f:
    for x in f.readlines():
        idx = x.find('=')
 
        variable = x[:idx]
        value = x[idx + 1:]
 
        exec("%s = %d" % (variable, int(value)))

a = random.randint(2, p - 1)
b = random.randint(2, p - 1)
sk = fast_pow(fast_pow(g, a, p), b, p)

with open('public_msg.txt', 'a') as f:
    f.write(str(sk))

with open('public_msg.txt', 'a') as f:
    f.write('\n' + str(g))