from math import gcd
from MATRICES import INDICE, INVERSE_MODULO, gp, gp_inverse

ALPHABET=[chr(i) for i in range(32,127)]
w=len(ALPHABET)
Tab=[chr(i) for i in range(32)]+[chr(i) for i in range(127,256)]
#FONCTIONS PRELIMINAIRES
def FILTRER(message):
    for c in Tab:
        msg=message.replace(c,"")
        message=msg
    return msg

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
    dic[pos]=INDICE(ALPHABET,c)
    pos=(pos+1)%w
  for c in ALPHABET:
    if(key.count(c)==0):
      rest+=c
  for c in rest:
    dic[pos]=INDICE(ALPHABET,c)
    pos=(pos+1)%w

  return dic


#CHIFFRE CLASSIQUES
def CHIFFRE_DE_CESAR(message,k):
    chiffré=""
    msg=FILTRER(message)
    for i in range(len(msg)):
        x=INDICE(ALPHABET,msg[i])
        y=x+k
        c=ALPHABET[y%w]
        chiffré+=c
    return chiffré
def DECHIFFREMENT_DE_CESAR(chiffré,k):
    p=(w-k)%w
    return CHIFFRE_DE_CESAR(chiffré,p)

def DECALAGE_AFFINE(message,a,b):
    chiffré=""
    msg=FILTRER(message)
    for i in range(len(msg)):
        x=INDICE(ALPHABET,msg[i])
        y=a*x+b
        c=ALPHABET[y%w]
        chiffré+=c
    return chiffré
def DECHIFFREMENT_DE_DECALAGEAFFINE(chiffré,a,b):
    a1=INVERSE_MODULO(a,w)
    b1=0-a1*b
    return DECALAGE_AFFINE(chiffré,a1,b1)

def CHIFFRE_DE_VIGENERE(message,key):
    chiffré=""
    msg=FILTRER(message)
    tmp=GENERE_CLE(key,len(msg))
    if len(tmp)!=len(msg):
        print("erreur")
    else:
        for i in range(len(msg)):
            x=INDICE(ALPHABET,msg[i])
            k=INDICE(ALPHABET,tmp[i])
            y=x+k
            chiffré+=ALPHABET[y%w]
    return chiffré
def DECHIFFREMENT_VIGENERE(chiffré,key):
    Tabclaire=list()
    for i in range(len(key)):
        Ci=chiffré[i:len(chiffré):len(key)]
        Mi=DECHIFFREMENT_DE_CESAR(Ci,INDICE(ALPHABET,key[i]))
        Tabclaire.append(Mi)
    messageclaire=RECOLLER(Tabclaire)
    return messageclaire
def DECALAGE_AFFINE_PAR_BLOC(message,a,b,p):
    if(gcd(a,w**p)!=1): print("error:Vous devez chiffrer avec un a inversible modulo",w**p)
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
            x=gp(Mi,w)
            y=(a*x+b)%w**p
            Ci=gp_inverse(y,p,w)
            for j in Ci:
                chiffré+=ALPHABET[j]
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
                msgclaire+=ALPHABET[j]
        return msgclaire
def CHIFFRE_PAR_PERMUTATION(message,key,p):
    chiffré=""
    msg=FILTRER(message)
    D=DICO_GENERATEUR(key,p)
    for c in msg:
        x=INDICE(ALPHABET,c)
        y=D[x]
        chiffré+=ALPHABET[y]

    return chiffré

def DECHIFFREMENT_PERMUTATION(chiffré,key,p):
    msgclaire=""
    D=DICO_GENERATEUR(key,p)
    for c in chiffré:
        y=INDICE(ALPHABET,c)
        for i in range(w):
            if(D[i]==y):
                x=i
        msgclaire+=ALPHABET[x]
    return msgclaire
def CHIFFRE_DE_VERNAM(message,key):
    chiffré=""
    msg=FILTRER(message)
    ky=FILTRER(key)
    if(len(msg)!=len(ky)):print("error:Le message et la clé doivent avoir la meme longueur:")
    else:
        for i in range(len(msg)):
            x=INDICE(ALPHABET,msg[i])
            k=INDICE(ALPHABET,ky[i])
            y=x+k
            chiffré+=ALPHABET[y%w]
    return chiffré
def DECHIFFREMENT_VERNAM(chiffré,key):
    msgclaire=""
    ky=FILTRER(key)
    if(len(chiffré)!=len(ky)):print("error:Le chiffré et la clé doivent avoir la meme longueur:")
    else:
        for i in range(len(chiffré)):
            x=INDICE(ALPHABET,chiffré[i])
            k=INDICE(ALPHABET,ky[i])
            y=x-k
            msgclaire+=ALPHABET[y%w]
    return msgclaire
#CRYPTANALYSE













#TESTS
m="rien ne se perd tout ce transforme.c'est ce qu'affirmait lavoisier."
print("---------------------")
C1=CHIFFRE_DE_CESAR(m,5)
print(C1)
print(DECHIFFREMENT_DE_CESAR(C1,5))
print("----------------------")
C2=DECALAGE_AFFINE(m,7,5)
print(C2)
print(DECHIFFREMENT_DE_DECALAGEAFFINE(C2,7,5))
print("---------------------")
C3=CHIFFRE_DE_VIGENERE(m,"marc")
print(C3)
print(DECHIFFREMENT_VIGENERE(C3,"marc"))
print("---------------------")
C4=DECALAGE_AFFINE_PAR_BLOC(m,17,40,2)
print(C4)
print(DECHIFFREMENT_AFFINE_PAR_BLOC(C4,17,40,2))
print("---------------------")
C5=CHIFFRE_PAR_PERMUTATION(m,"crossword",10)
print(C5)
print(DECHIFFREMENT_PERMUTATION(C5,"crossword",10))
print("-----------------------")
C6=CHIFFRE_DE_VERNAM(m,m)
print(C6)
print(DECHIFFREMENT_VERNAM(C6,m))