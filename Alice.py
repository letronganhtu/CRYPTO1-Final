with open('parameter.txt', encoding = 'utf-8') as f:
    for x in f.readlines():
        idx = x.find('=')
 
        variable = x[:idx]
        value = x[idx + 1:]
 
        exec("%s = %d" % (variable, int(value)))
 
import random
import socket
 
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
 
def setup_key():
    sk_Alice = random.randint(2, p - 1)
    dlp_Alice = fast_pow_mod(g, sk_Alice, p)
    s.send(str(dlp_Alice).encode())
    dlp_Bob = int(s.recv(1024).decode())
    return fast_pow_mod(dlp_Bob, sk_Alice, p);
 
sk_communicate = setup_key()
 
while True:
    Alice_msg = input("Alice: ")
    s.send(Alice_msg.encode())
    Bob_msg = s.recv(1024)
    print("Bob:", Bob_msg.decode())
 
s.close()