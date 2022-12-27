import numpy as np
from sympy import Matrix

# def matInvMod (vmnp, mod=251):
#     nr = vmnp.shape[0]
#     nc = vmnp.shape[1]
#     if (nr!= nc):
#         print ("Error: Non square matrix! exiting")
#         exit()
#     vmsym = Matrix(vmnp)
#     vmsymInv = vmsym.inv_mod(mod)
#     vmnpInv = np.array(vmsymInv)
#     return vmnpInv

def matInvMod (vmnp, mod):
    nr = vmnp.shape[0]
    nc = vmnp.shape[1]
    if (nr!= nc):
        print ("Error: Non square matrix! exiting")
        exit()
    vmsym = Matrix(vmnp)
    vmsymInv = vmsym.inv_mod(mod)
    vmnpInv = np.array(vmsymInv)
    return vmnpInv

def encrypt(m, sk_communicate):
    mchar = np.array([ord(x) for x in m])
    i = 0
    j = 12
    me = []
    while j < len(m):
        me.append(mchar[i:j].reshape(12, 1))
        i = j
        j += 12
    if i < len(m):
        me.append(mchar[i:].reshape(len(m) - i, 1))
    
    cipher = np.array([sk_communicate @ x if x.shape[0] == 12 else x for x in me],dtype=object)
    ciphertext = []
    for i in range(len(cipher)):
        cipher[i] = cipher[i] % 251
        for j in range(len(cipher[i])):
            ciphertext.append(chr(cipher[i][j][0]))
    return ''.join(ciphertext)

def decrypt(cipher, sk_inv):

    mchar = np.array([ord(x) for x in cipher])
    i = 0
    j = 12
    me = []
    while j < len(cipher):
        me.append(mchar[i:j].reshape(12, 1))
        i = j
        j += 12
    if i < len(cipher):
        me.append(mchar[i:].reshape(len(cipher) - i, 1))

    plain = [sk_inv @ x if x.shape[0] == 12 else x for x in me]
    plainC = []
    for p in plain:
            for x in p:
                plainC.append(chr(int(x[0] % 251)))

    return ''.join(plainC)
