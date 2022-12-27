with open('parameter.txt', encoding = 'utf-8') as f:
    for x in f.readlines():
        idx = x.find('=')
 
        variable = x[:idx]
        value = x[idx + 1:]
 
        exec("%s = %d" % (variable, int(value)))
 
import random
import socket
import numpy as np

from digitalSignature import RSAsign, RSAverify
from encrypt_decrypt import encrypt, decrypt, matInvMod
 
s = socket.socket()
s.connect(("localhost", 1203))

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
    sk_Alice = random.randint(2, p - 1)
    dlp_Alice = fast_pow_mod(g, sk_Alice, p)
    s.send(str(dlp_Alice).encode())
    dlp_Bob = int(s.recv(1024).decode())
    sk = fast_pow_mod(dlp_Bob, sk_Alice, p)
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
sk_communicate = sk_communicate.astype(int)
sk_inv = matInvMod(sk_communicate, 251)
sk_inv = sk_inv % 251
block_size = 12
print(sk_communicate)

while True:
    msg_inp = input("Alice: ")
    Alice_msg = encrypt(msg_inp, sk_communicate)
    s.send(Alice_msg.encode(encoding='utf-8'))
    s.send(str(RSAsign(msg_inp, d, n)).encode())
    msg_inp = s.recv(1024).decode(encoding='utf-8')
    sign = int(s.recv(1024).decode())
    print("sign of message: ", sign)
    Bob_msg = decrypt(msg_inp, sk_inv)
    if RSAverify(Bob_msg, sign, e, n):
        print("Bob:", Bob_msg)
    else:
        print("message was changed")
    count_message += 2
    if count_message == 10:
        sk_communicate = setup_key(g, p)
        count_message = 0
        print(sk_communicate)
 
s.close()