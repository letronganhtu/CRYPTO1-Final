with open('parameter.txt', encoding = 'utf-8') as f:
    for x in f.readlines():
        idx = x.find('=')
 
        variable = x[:idx]
        value = x[idx + 1:]
 
        exec("%s = %d" % (variable, int(value)))

with open('public_msg.txt', 'w') as f:
    pass
 
import random
import socket
import numpy as np
from digitalSignature import RSAsign, RSAverify, genRSA, fast_pow_mod
from encrypt_decrypt import encrypt, decrypt, matInvMod
 
s = socket.socket()
s.connect(("localhost", 1203))

count_message = 0

e, d, n = genRSA(512)
s.send(str(e).encode())
eB = int(s.recv(1024).decode())
s.send(str(n).encode())
nB = int(s.recv(1024).decode())

with open('public_msg.txt', 'a') as f:
    f.write('eA=' + str(e) + '\n')
    f.write('nA=' + str(n) + '\n')
    f.write('eB=' + str(eB) + '\n')
    f.write('nB=' + str(nB) + '\n')

def setup_key(g, p):
    sk_Alice = random.randint(2, p - 1)
    dlp_Alice = fast_pow_mod(g, sk_Alice, p)

    s.send(str(dlp_Alice).encode())
    dlp_Bob = int(s.recv(1024).decode())
    with open('public_msg.txt', 'a') as f:
        f.write('g^a=' + str(dlp_Alice) + '\n')
        f.write('g^b=' + str(dlp_Bob) + '\n')

    sk = fast_pow_mod(dlp_Bob, sk_Alice, p)

    # Create key_matrix
    L = np.zeros((12, 12))
    U = np.zeros((12, 12))

    # Generate diag(L)
    for i in range(0, 12):
        temp1 = sk % 100
        sk = sk // 100
        while temp1 == 0:
            temp1 = sk % 100
            sk = sk // 100
        L[i][i] = temp1

    # Generate diag(U)
    for i in range(0, 12):
        temp1 = sk % 100
        sk = sk // 100
        while temp1 == 0:
            temp1 = sk % 100
            sk = sk // 100
        U[i][i] = temp1

    # Generate L, R (L: i > j && R: i < j)
    for i in range(0, 12):
        for j in range(i + 1, 12):
            U[i][j] = sk % 100
            sk = sk // 100
            if sk == 0: sk = 1
            L[j][i] = sk % 100
            sk = sk // 100
            if sk == 0: sk = 101

    key_matrix = np.dot(L, U)
    for i in range(0, 12):
        for j in range(0, 12):
            key_matrix[i][j] %= 251
    return key_matrix

sk_communicate = setup_key(g, p)
sk_communicate = sk_communicate.astype(int)
sk_inv = matInvMod(sk_communicate, 251)
sk_inv = sk_inv % 251

print(sk_communicate)

while True:
    msg_inp = input("Alice: ")
    Alice_msg = encrypt(msg_inp, sk_communicate)
    s.send(Alice_msg.encode(encoding='utf-8'))
    s.send(str(RSAsign(msg_inp, d, n)).encode())
    with open('public_msg.txt', 'a') as f:
        f.write('(cA || sA)=(' + Alice_msg + ' || ' + str(RSAsign(msg_inp, d, n)) + ')' + '\n')

    msg_inp = s.recv(1024).decode(encoding='utf-8')
    sign = int(s.recv(1024).decode())
    Bob_msg = decrypt(msg_inp, sk_inv)
    if RSAverify(Bob_msg, sign, eB, nB):
        print("Bob:", Bob_msg)
    else:
        print("Notification: Message is not belong to Bob")
    with open('public_msg.txt', 'a') as f:
        f.write('(cB || sB)=(' + str(msg_inp) + ' || ' + str(sign) + ')' + '\n')
        
    count_message += 2
    if count_message == 10:
        sk_communicate = setup_key(g, p)
        count_message = 0
        print(sk_communicate)

f.close()
s.close()