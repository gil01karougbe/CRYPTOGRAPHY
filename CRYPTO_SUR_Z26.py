from math import gcd
from numpy.linalg import inv, det
import numpy as np
from index import INDICE, MAX, gp, gp_inverse
from index import INVERSE_MODULO

Tab=[chr(i) for i in range(97)] + [chr(i) for i in range(123,256)]
ALPHABET26=[chr(i) for i in range(97,123)]
#FONCTIONS PRELIMINAIRES
def FILTRER(message):
    for c in Tab:
        msg=message.replace(c,"")
        message=msg
    return msg
def GENERE_CLE(cle,N):
    k=FILTRER(cle)
    q=N//len(k)
    r=N%len(k)
    key=q*k
    if r==0:
        return key
    else:
        for i in range(r):
            key+=k[i]

        return key
def RECOLLER(liste):
    f = ''
    try : #clause try
        for i in range (len(liste[0])):
            for z in liste: f += z[i]
    except :#clause except
        pass    #l'instruction pass indique de rien faire ici quelque soit le type d'exception
    return f
def DICO_GENERATEUR(keyword,pos):
  key=""
  rest=""
  dic={

  }
  i=0
  for c in keyword:
    k=keyword[:i]
    if(k.count(c)==0):
      key+=c
    i=i+1
  for c in key:
    dic[pos]=INDICE(ALPHABET26,c)
    pos=(pos+1)%26
  for c in ALPHABET26:
    if(key.count(c)==0):
      rest+=c
  for c in rest:
    dic[pos]=INDICE(ALPHABET26,c)
    pos=(pos+1)%26

  return dic

#LES CHIFFRES CLASSIQUE
def CHIFFRE_DE_CESAR(message,k):
    chiffré=""
    msg=FILTRER(message)
    for c in msg:
        x=INDICE(ALPHABET26,c)
        y=x+k
        chiffré+=ALPHABET26[y%26]
    return chiffré
def DECHIFFREMENT_DE_CESAR(chiffré,k):
    p=(26-k)%26
    return CHIFFRE_DE_CESAR(chiffré,p)



def DECALAGE_AFFINE(message,a,b):
    chiffré=""
    msg=FILTRER(message)
    for i in range(len(msg)):
        x=INDICE(ALPHABET26,msg[i])
        y=a*x+b
        chiffré+=ALPHABET26[y%26]
    return chiffré
def DECHIFFREMENT_DE_DECALAGEAFFINE(chiffré,a,b):
    a1=INVERSE_MODULO(a,26)
    b1=0-a1*b
    return DECALAGE_AFFINE(chiffré,a1,b1)


def CHIFFRE_PAR_PERMUTATION(message,key,p):
    chiffré=""
    msg=FILTRER(message)
    D=DICO_GENERATEUR(key,p)
    for c in msg:
        x=INDICE(ALPHABET26,c)
        y=D[x]
        chiffré+=ALPHABET26[y]

    return chiffré
def DECHIFFREMENT_PERMUTATION(chiffré,key,p):
    msgclaire=""
    D=DICO_GENERATEUR(key,p)
    for c in chiffré:
        y=INDICE(ALPHABET26,c)
        for i in range(26):
            if(D[i]==y):
                x=i
        msgclaire+=ALPHABET26[x]
    return msgclaire


def CHIFFRE_DE_VIGENERE(message,key):
    chiffré=""
    msg=FILTRER(message)
    tmp=GENERE_CLE(key,len(msg))
    if len(tmp)!=len(msg):
        print("erreur")
    else:
        for i in range(len(msg)):
            x=INDICE(ALPHABET26,msg[i])
            k=INDICE(ALPHABET26,tmp[i])
            y=x+k
            chiffré+=ALPHABET26[y%26]
    return chiffré
def DECHIFFREMENT_VIGENERE(chiffré,key):
    Tabclaire=list()
    for i in range(len(key)):
        Ci=chiffré[i:len(chiffré):len(key)]
        Mi=DECHIFFREMENT_DE_CESAR(Ci,INDICE(ALPHABET26,key[i]))
        Tabclaire.append(Mi)
    messageclaire=RECOLLER(Tabclaire)
    return messageclaire


def DECALAGE_AFFINE_PAR_BLOC(message,a,b,p):
    if(gcd(a,26**p)!=1): print("error:Vous devez chiffrer avec un a inversible modulo",26**p)
    else:
        msg=FILTRER(message)
        chiffré=""
        n=len(msg)
        tmp=n%p
        if(tmp!=0):
            msg.rjust(n+p-tmp,"x")
        r=len(msg)//p
        for i in range(r):
            Mi=msg[i*p:(i+1)*p]
            x=gp(Mi,26)
            y=(a*x+b)%26**p
            Ci=gp_inverse(y,p,26)
            for j in Ci:
                chiffré+=ALPHABET26[j]
        return chiffré
def DECHIFFREMENT_AFFINE_PAR_BLOC(chiffré,a,b,p):
    msgclaire=""
    if(gcd(a,26**p)!=1): print("error:")
    else:
        a1=INVERSE_MODULO(a,26**p)
        r=len(chiffré)//p
        for i in range(r):
            Ci=chiffré[i*p:(i+1)*p]
            y=gp(Ci,26)
            x=(a1*y-a1*b)%26**p
            Mi=gp_inverse(x,p,26)
            for j in Mi:
                msgclaire+=ALPHABET26[j]
        return msgclaire


def CHIFFRE_DE_HILL(message,K):
    chiffré=""
    T=[]
    (p,q)= np.shape(K)
    msg=FILTRER(message)
    while (len(msg)%p!=0):
        msg+="x"
    for c in msg:
        x=INDICE(ALPHABET26,c)
        T.append(x)
    n=len(T)//p
    tmp=np.array(T)
    X=tmp.reshape(n,p)
    Y=np.dot(X,K)
    R=list(Y.reshape(n*p))
    for i in R:
        j=int(i)
        c=ALPHABET26[j%26]
        chiffré+=c
    return chiffré
def DECHIFFREMENT_HILL(chiffré,K):
    K1=inv(K)
    return CHIFFRE_DE_HILL(chiffré,K1)


def CHIFFRE_DE_VERNAM(message,key):
    chiffré=""
    msg=FILTRER(message)
    ky=FILTRER(key)
    if(len(msg)!=len(ky)):print("error:Le message et la clé doivent avoir la meme longueur:")
    else:
        for i in range(len(msg)):
            x=INDICE(ALPHABET26,msg[i])
            k=INDICE(ALPHABET26,ky[i])
            y=x+k
            chiffré+=ALPHABET26[y%26]
    return chiffré
def DECHIFFREMENT_VERNAM(chiffré,key):
    msgclaire=""
    ky=FILTRER(key)
    if(len(chiffré)!=len(ky)):print("error:Le chiffré et la clé doivent avoir la meme longueur:")
    else:
        for i in range(len(chiffré)):
            x=INDICE(ALPHABET26,chiffré[i])
            k=INDICE(ALPHABET26,ky[i])
            y=x-k
            msgclaire+=ALPHABET26[y%26]
    return msgclaire

#CRYPANALYSE
def CRYPTANALYSE_CESAR(chiffré):
    T=[]
    for c in ALPHABET26:
        n=chiffré.count(c)
        T.append(n)
    (i1,m1)=MAX(T)
    #conjecture1
    p=(i1-4)%26
    mc=DECHIFFREMENT_DE_CESAR(chiffré,p)
    if(CHIFFRE_DE_CESAR(mc)==chiffré):return mc
    else:
        T.remove(m1)
        #conjecture2
        (i2,m2)=MAX(T)    



#TEST
m="rien ne se perd tout ce transforme.c'est ce qu'affirmait lavoisier."
print("CESAR---------------------")
C1=CHIFFRE_DE_CESAR(m,5)
print(C1)
print(DECHIFFREMENT_DE_CESAR(C1,5))
print("DECALAGE AFFINE----------------------")
C2=DECALAGE_AFFINE(m,7,5)
print(C2)
print(DECHIFFREMENT_DE_DECALAGEAFFINE(C2,7,5))
print("VIGENERE---------------------")
C3=CHIFFRE_DE_VIGENERE(m,"marc")
print(C3)
print(DECHIFFREMENT_VIGENERE(C3,"marc"))
print("AFFINE PAR BLOC---------------------")
C4=DECALAGE_AFFINE_PAR_BLOC(m,17,40,2)
print(C4)
print(DECHIFFREMENT_AFFINE_PAR_BLOC(C4,17,40,2))
print("PERMUTATION---------------------")
C5=CHIFFRE_PAR_PERMUTATION(m,"crossword",10)
print(C5)
print(DECHIFFREMENT_PERMUTATION(C5,"crossword",10))
print("HILL-----------------------")
key=[[1,2],
    [3,7]]
k=np.array(key)
C6=CHIFFRE_DE_HILL(m,k)
print(C6)
print(DECHIFFREMENT_HILL(C6,k))
print("VERNAM---------------------")
C7=CHIFFRE_DE_VERNAM(m,m)
print(C7)
print(DECHIFFREMENT_VERNAM(C7,m))

