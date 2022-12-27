with open('parameter.txt', encoding = 'utf-8') as f:
    for x in f.readlines():
        idx = x.find('=')
 
        variable = x[:idx]
        value = x[idx + 1:]
 
        exec("%s = %d" % (variable, int(value)))
 
import random
import socket
import numpy as np

host = 'localhost'
port = 1203
 
s = socket.socket()
s.bind((host, port))
s.listen(1)
c, addr = s.accept()
 
def fast_pow_mod(a, b, p):
    res = 1
    while b:
        if b % 2 == 1:
            res = (res * a) % p
        a = (a * a) % p
        b = b // 2
    return res

count_message = 0
 
def setup_key(g, p):
    sk_Bob = random.randint(2, p - 1)
    dlp_Bob = fast_pow_mod(g, sk_Bob, p)
    dlp_Alice = int(c.recv(1024).decode())
    c.send(str(dlp_Bob).encode())
    sk = fast_pow_mod(dlp_Alice, sk_Bob, p)
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
    return key_matrix
 
sk_communicate = setup_key(g, p)
block_size = 12
print(sk_communicate)

while True:
    Alice_msg = c.recv(1024)
    print("Alice:", Alice_msg.decode())
    Bob_msg = input("Bob: ")
    c.send(Bob_msg.encode())
    count_message += 2
    if count_message == 10:
        sk_communicate = setup_key(g, p)
        count_message = 0
        print(sk_communicate)
 
c.close()