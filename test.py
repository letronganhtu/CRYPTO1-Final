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
temp = sk
L = np.zeros((12, 12))
U = np.zeros((12, 12))

# Generate diag(L)
for i in range(0, 12):
    temp1 = temp % 100
    temp = temp // 100
    while temp1 == 0:
        temp1 = temp % 100
        temp = temp // 100
    L[i][i] = temp1

# Generate diag(R)
for i in range(0, 12):
    temp1 = temp % 100
    temp = temp // 100
    while temp1 == 0:
        temp1 = temp % 100
        temp = temp // 100
    U[i][i] = temp1

# Generate L, R -> L: i > j, R: i < j
for i in range(0, 12):
    for j in range(i + 1, 12):
        U[i][j] = temp % 100
        temp = temp // 100
        if temp == 0: temp = 1
        L[j][i] = temp % 100
        temp = temp // 100
        if temp == 0: temp = 101

key_matrix = np.dot(L, U)
for i in range(0, 12):
    for j in range(0, 12):
        key_matrix[i][j] %= 251
print(key_matrix)