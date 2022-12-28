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

count_message = 0
pA = 113658436785139662796223136980555068607462604577987509636788088080318546081514054104144409693326063583110947795205652085425805184552119018806609211242120470814388980461297179573847102907483713541247287395008519163649641393142474317297199404053596942261356796340996425471596388415961886902706565659923727624289
qA = 160050402698988181905146140298688795269418737468199439444518303182550992095086837450584681179863645857391629240427926284717274826061590968333848421812794053900873953602679011201323898335266657577891434675457278660109652028758270302689559536597767355295287742730553336614733681243077527136655401631967487106987
phiA = (pA - 1) * (qA - 1)

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
    sk_Alice = random.randint(2, p - 1)
    dlp_Alice = fast_pow_mod(g, sk_Alice, p)

    s.send(str(dlp_Alice).encode())

    dlp_Bob = int(s.recv(1024).decode())

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
dA = pow(eA, -1, phiA)

print(sk_communicate)

while True:
    msg_inp = input("Alice: ")
    Alice_msg = encrypt(msg_inp, sk_communicate)
    s.send(Alice_msg.encode(encoding = 'utf-8'))
    s.send(str(RSAsign(msg_inp, dA, nA)).encode())

    msg_inp = s.recv(1024).decode(encoding = 'utf-8')
    sign_B = int(s.recv(1024).decode())
    Bob_msg = decrypt(msg_inp, sk_inv)
    if RSAverify(Bob_msg, sign_B, eB, nB):
        print("Bob:", Bob_msg)
    else:
        print("Notification: Message is not belong to Bob")

    count_message += 2
    if count_message == 10:
        sk_communicate = setup_key(g, p)
        count_message = 0
        print(sk_communicate)
 
s.close()