from math import gcd
from index import INDICE, INVERSE_MODULO, gp, gp_inverse
import numpy as np
from numpy.linalg import inv, det
Tab=[chr(i) for i in range(256)]
w=len(Tab)
#FONCTIONS PRELIMINAIRES
def GENERE_CLE(cle,N):
    q=N//len(cle)
    r=N%len(cle)
    key=q*cle
    if r==0:
        return key
    else:
        for i in range(r):
            key+=cle[i]

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
    dic[pos]=INDICE(Tab,c)
    pos=(pos+1)%w
  for c in Tab:
    if(key.count(c)==0):
      rest+=c
  for c in rest:
    dic[pos]=INDICE(Tab,c)
    pos=(pos+1)%w

  return dic
#LES CHIFFRES CLASSIQUES

def CHIFFRE_DE_CESAR(message,k):
    chiffré=""
    for c in message:
        x=INDICE((Tab),c)
        y=x+k
        chiffré+=Tab[y%w]
    return chiffré
def DECHIFFREMENT_DE_CESAR(chiffré,k):
    p=(w-k)%w
    return CHIFFRE_DE_CESAR(chiffré,p)


def DECALAGE_AFFINE(message,a,b):
    chiffré=""
    for i in range(len(message)):
        x=INDICE(Tab,message[i])
        y=a*x+b
        chiffré+=Tab[y%w]
    return chiffré
def DECHIFFREMENT_DE_DECALAGEAFFINE(chiffré,a,b):
    a1=INVERSE_MODULO(a,w)
    b1=0-a1*b
    return DECALAGE_AFFINE(chiffré,a1,b1)


def CHIFFRE_PAR_PERMUTATION(message,key,p):
    chiffré=""
    D=DICO_GENERATEUR(key,p)
    for c in message:
        x=INDICE(Tab,c)
        y=D[x]
        chiffré+=Tab[y]

    return chiffré
def DECHIFFREMENT_PERMUTATION(chiffré,key,p):
    msgclaire=""
    D=DICO_GENERATEUR(key,p)
    for c in chiffré:
        y=INDICE(Tab,c)
        for i in range(w):
            if(D[i]==y):
                x=i
        msgclaire+=Tab[x]
    return msgclaire


def CHIFFRE_DE_VIGENERE(message,key):
    chiffré=""
    tmp=GENERE_CLE(key,len(message))
    if len(tmp)!=len(message):
        print("erreur")
    else:
        for i in range(len(message)):
            x=INDICE(Tab,message[i])
            k=INDICE(Tab,tmp[i])
            y=x+k
            chiffré+=Tab[y%w]
    return chiffré
def DECHIFFREMENT_VIGENERE(chiffré,key):
    Tabclaire=list()
    for i in range(len(key)):
        Ci=chiffré[i:len(chiffré):len(key)]
        Mi=DECHIFFREMENT_DE_CESAR(Ci,INDICE(Tab,key[i]))
        Tabclaire.append(Mi)
    messageclaire=RECOLLER(Tabclaire)
    return messageclaire



def DECALAGE_AFFINE_PAR_BLOC(message,a,b,p):
    if(gcd(a,w**p)!=1): print("error:Vous devez chiffrer avec un a inversible modulo",w**p)
    else:
        chiffré=""
        n=len(message)
        tmp=n%p
        if(tmp!=0):
            message.rjust(n+p-tmp,"x")
        r=len(message)//p
        for i in range(r):
            Mi=message[i*p:(i+1)*p]
            x=gp(Mi,w)
            y=(a*x+b)%w**p
            Ci=gp_inverse(y,p,w)
            for j in Ci:
                chiffré+=Tab[j]
        return chiffré
def DECHIFFREMENT_AFFINE_PAR_BLOC(chiffré,a,b,p):
    msgclaire=""
    if(gcd(a,w**p)!=1): print("error:")
    else:
        a1=INVERSE_MODULO(a,w**p)
        r=len(chiffré)//p
        for i in range(r):
            Ci=chiffré[i*p:(i+1)*p]
            y=gp(Ci,w)
            x=(a1*y-a1*b)%w**p
            Mi=gp_inverse(x,p,w)
            for j in Mi:
                msgclaire+=Tab[j]
        return msgclaire



def CHIFFRE_DE_HILL(message,K):
    chiffré=""
    T=[]
    (p,q)= np.shape(K)
    while(len(message)%p!=0):
        message+="x"
    for c in message:
        x=INDICE(Tab,c)
        T.append(x)
    n=len(T)//p
    tmp=np.array(T)
    X=tmp.reshape(n,p)
    Y=np.dot(X,K)
    R=list(Y.reshape(n*p))
    for i in R:
        j=int(i)
        c=Tab[j%w]
        chiffré+=c
    return chiffré
def DECHIFFREMENT_HILL(chiffré,K):
    K1=inv(K)
    return CHIFFRE_DE_HILL(chiffré,K1)



def CHIFFRE_DE_VERNAM(message,key):
    chiffré=""
    if(len(message)!=len(key)):print("error:Le message et la clé doivent avoir la meme longueur:")
    else:
        for i in range(len(message)):
            x=INDICE(Tab,message[i])
            k=INDICE(Tab,key[i])
            y=x+k
            chiffré+=Tab[y%w]
    return chiffré
def DECHIFFREMENT_VERNAM(chiffré,key):
    msgclaire=""
    if(len(chiffré)!=len(key)):print("error:Le chiffré et la clé doivent avoir la meme longueur:")
    else:
        for i in range(len(chiffré)):
            x=INDICE(Tab,chiffré[i])
            k=INDICE(Tab,key[i])
            y=x-k
            msgclaire+=Tab[y%w]
    return msgclaire

#CRYPTANALYSE




























#TESTS
m="rien ne se perd tout ce transforme.c'est ce qu'affirmait lavoisier."
print("---------------------\n")
C1=CHIFFRE_DE_CESAR(m,5)
print(C1)
print(DECHIFFREMENT_DE_CESAR(C1,5))
print("----------------------\n")
C2=DECALAGE_AFFINE(m,7,5)
print(C2)
print(DECHIFFREMENT_DE_DECALAGEAFFINE(C2,7,5))
print("---------------------\n")
C3=CHIFFRE_DE_VIGENERE(m,"marc")
print(C3)
print(DECHIFFREMENT_VIGENERE(C3,"marc"))
print("---------------------\n")
C4=DECALAGE_AFFINE_PAR_BLOC(m,17,40,2)
print(C4)
print(DECHIFFREMENT_AFFINE_PAR_BLOC(C4,17,40,2))
print("---------------------\n")
C5=CHIFFRE_PAR_PERMUTATION(m,"crossword",10)
print(C5)
print(DECHIFFREMENT_PERMUTATION(C5,"crossword",10))
print("-----------------------\n")
key=[[1,2],
    [3,7]]
k=np.array(key)
C6=CHIFFRE_DE_HILL(m,k)
print(C6)
print(DECHIFFREMENT_HILL(C6,k))
print("---------------------")
C7=CHIFFRE_DE_VERNAM(m,m)
print(C7)
print(DECHIFFREMENT_VERNAM(C7,m))
