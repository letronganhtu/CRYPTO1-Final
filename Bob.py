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

host = 'localhost'
port = 1203
s = socket.socket()
s.bind((host, port))
s.listen(1)
c, addr = s.accept()

count_message = 0
pB = 179728538306884079398457288348066998853352219039249437614727251447184351686624955454911993858991754503372836656800209148393382934261699922823944185325286359123651842263657000411821183956578227605909850733106370988323885078636229785024164089093242384827872271748469181412837289310958657973628429440885905292237
qB = 134100871424245206782626629395231019933545892507830108674137289164362564793422418598265221112506337841272234726494910128486401814092625782372415463845746777117257199302532928137599901248609428017888868530802706435551627847656785891586772611020916107597543791601376633967071595969550122331247743592703682067187
phiB = (pB - 1) * (qB - 1)
 
def fast_pow_mod(a, b, p):
    res = 1
    while b:
        if b % 2 == 1:
            res = (res * a) % p
        a = (a * a) % p
        b = b // 2
    return res
 
def setup_key(g, p):
    # Setup private key
    sk_Bob = random.randint(2, p - 1)
    dlp_Bob = fast_pow_mod(g, sk_Bob, p)

    dlp_Alice = int(c.recv(1024).decode())

    c.send(str(dlp_Bob).encode())

    sk = fast_pow_mod(dlp_Alice, sk_Bob, p)

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
dB = pow(eB, -1, phiB)

print(sk_communicate)

while True:
    msg_inp = c.recv(1024)
    sign_A = int(c.recv(1024).decode())
    Alice_msg = decrypt(msg_inp.decode(encoding = 'utf-8'), sk_inv)
    if RSAverify(Alice_msg, sign_A, eA, nA):
        print("Alice:", Alice_msg)
    else:
        print("Notification: Message is not belong to Alice")

    msg_inp = input("Bob: ")
    Bob_msg = encrypt(msg_inp, sk_communicate)
    c.send(Bob_msg.encode(encoding = 'utf-8'))
    c.send(str(RSAsign(msg_inp, dB, nB)).encode())

    count_message += 2
    if count_message == 10:
        sk_communicate = setup_key(g, p)
        count_message = 0
        print(sk_communicate)
 
c.close()