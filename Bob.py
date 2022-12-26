with open('parameter.txt', encoding = 'utf-8') as f:
    for x in f.readlines():
        idx = x.find('=')
 
        variable = x[:idx]
        value = x[idx + 1:]
 
        exec("%s = %d" % (variable, int(value)))
 
import random
import socket
 
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
 
def setup_key():
    sk_Bob = random.randint(2, p - 1)
    dlp_Bob = fast_pow_mod(g, sk_Bob, p)
    dlp_Alice = int(c.recv(1024).decode())
    c.send(str(dlp_Bob).encode())
    return fast_pow_mod(dlp_Alice, sk_Bob, p)
 
sk_communicate = setup_key()
 
while True:
    Alice_msg = c.recv(1024)
    print("Alice:", Alice_msg.decode())
    Bob_msg = input("Bob: ")
    c.send(Bob_msg.encode())
 
c.close()