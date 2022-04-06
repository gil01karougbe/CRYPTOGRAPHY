from math import gcd
import numpy

ALPHABET26=[chr(i) for i in range(97,123)]
ALPHABET27=[chr(i) for i in range(97,123)]+[chr(32)]
ALPHABET=[chr(i) for i in range(32,127)]
w=len(ALPHABET)
Tab=[chr(i) for i in range(256)]
t=len(Tab)

def INVERSE_MODULO(X,N):
  if(gcd(X,N)!=1): print("error")
  else:
    for a in range(N):
      if(X*a%N==1): return a

def INDICE(T,X):
    for j in range(len(T)):
        if T[j]==X:
            return j
    
def gp(chaine,N):
  S=0
  k=len(chaine)-1
  if(N==26):
    for c in chaine:
      a=INDICE(ALPHABET26,c)
      S=S+a*(N**k)
      k=k-1
    return S
  if(N==27):
    for c in chaine:
      a=INDICE(ALPHABET27,c)
      S=S+a*(N**k)
      k=k-1
    return S
  if(N==w):
    for c in chaine:
      a=INDICE(ALPHABET,c)
      S=S+a*(N**k)
      k=k-1
    return S
  if(N==t):
    for c in chaine:
      a=INDICE(Tab,c)
      S=S+a*(N**k)
      k=k-1
    return S

def gp_inverse(Y,p,N):
  R=[]
  for i in range(p-1,-1,-1):
    q=Y//N**i
    R.append(q)
    Y=Y%N**i
  return R

def MAX(T):
  max=T[0]
  for i in T:
    if i>max:max=i
  j=T.index(max)  
  return (j,max)
