import numpy as np
import numpy as np
import matplotlib.pyplot as plt
from copy import deepcopy
plt.interactive(True)
fig, ax = plt.subplots()

global Dname

Dname={}

def inter(a,b):
    c=[]
    for elem in b:
        if elem in a:
            c.append(elem)
    return c
    
    

class Sud():  #tableau, pave, case
    def __init__(self):
        self.tab=np.array([[np.zeros((3,3)) for i in range(3)] for i in range(3)])
        self.possibles={}
        self.text=np.array([[[[ax.text(3*j+l+0.5, (3-i)*3-k-0.5, '') for l in range(3)] for k in range(3)] for j in range(3)] for i in range(3)])
        for i in range(3):
            for j in range(3):
                for k in range(3):
                    for l in range(3):
                        self.possibles[(i,j,k,l)]=[]
                        
    def getpave(self,i,j):  #i,j sont les coordonnées du pavé
        L=[i for i in range(1,10)]
        for k in range(3):
            for l in range(3):
                x=self.tab[i,j,k,l]
                if x!=0:
                    if x in L:
                        L.remove(x)
                    else: 
                        return []
        return L
    def getligne(self,i,j,k): #k numéro de la colonnz du pavé
        L=[i for i in range(1,10)]
        for l0 in range(9):
            x=self.tab[i,l0//3,k,l0%3]
            if x!=0:
                if x in L:
                    L.remove(x)
                else: 
                    return []
        return L
    def getcolonne(self,i,j,l): #l numéro de la ligne du pavé
        L=[i for i in range(1,10)]
        for k0 in range(9):
            x=self.tab[k0//3,j,k0%3,l]
            if x!=0:
                if x in L:
                    L.remove(x)
                else: 
                    return []
        return L
    
    def valpossible(self,i,j,k,l): #retourne la liste des valeurs VIDE si il y a erreur
        return inter(self.getpave(i,j),inter(self.getligne(i,j,k),self.getcolonne(i,j,l)))
        
    def updatedic(self):
        c=False
        for i in range(3):
            for j in range(3):
                for k in range(3):
                    for l in range(3):
                        if self.tab[i,j,k,l]==0:
                            L=self.valpossible(i,j,k,l)
                            if len(L)==1:
                                self.tab[i,j,k,l]=L[0]
                                self.text[i,j,k,l].set_text(str(int(self.tab[i,j,k,l])))
                                self.text[i,j,k,l].set_color('b')
                                # print(i,j,k,l)
                                c=True
                            else:
                                self.possibles[(i,j,k,l)]=L
        return c
    
    def remplissage(self): #RESOLUTION
        min_val, max_val = 0, 9
        ind_array = np.arange(min_val + 0.5, max_val + 0.5, 1.0)
        x, y = np.meshgrid(ind_array, ind_array)
        
        self.affichefirst()
        
        ax.set_xlim(min_val, max_val)
        ax.set_ylim(min_val, max_val)
        ax.set_xticks(np.arange(max_val))
        ax.set_yticks(np.arange(max_val))
        ax.grid()
   
        c=True
        while c==True:
            c=self.updatedic()
        plt.show()
        L=self.zero()
        if L!=[]:
            self.assume(L,1)
        # plt.pause(0.01)
            
    
        
    def affichefirst(self):
        
        for i in range(3):
            for j in range(3):
                for k in range(3):
                    for l in range(3):
                        x=self.tab[i,j,k,l]
                        if x!=0:
                            self.text[i,j,k,l].set_text(str(int(x)))
                            # self.text[i,j,k,l].set_color('k')
    def delete(self):
        for i in range(3):
            for j in range(3):
                for k in range(3):
                    for l in range(3):
                        self.text[i,j,k,l].set_text("")
                            # self.text[i,j,k,l].set_color('k')
        
    
                    
    def zero(self):  #retourne la liste des cases égales à zéro
        L=[]
        for i in range(3):
            for j in range(3):
                for k in range(3):
                    for l in range(3):
                        x=self.tab[i,j,k,l]
                        if x==0:
                            L.append([i,j,k,l])
        return L
        
    def updatedicassume(self): #0:pas de modif    1: modif     2:erreur 
        c=0
        for i in range(3):
            for j in range(3):
                for k in range(3):
                    for l in range(3):
                        if self.tab[i,j,k,l]==0:
                            L=self.valpossible(i,j,k,l)
                            if len(L)==1:
                                self.tab[i,j,k,l]=L[0]
                                self.text[i,j,k,l].set_text(str(int(self.tab[i,j,k,l])))
                                self.text[i,j,k,l].set_color('b')
                                # plt.pause(0.01)
                                c=1
                            elif len(L)==0:
                                return 2
                            else:
                                self.possibles[(i,j,k,l)]=L
        return c
        
    def assume(self,lzero,NUM):  #essaie la case ou self possible est minimal
        # print('ok')

        k00=2
        c=True
        while c:
            for elem in lzero:
                if c:
                    i,j,k,l=elem
                    length=len(self.possibles[(i,j,k,l)])

                    if length==k00:
                        # print('ok')
                        return self.tryval(i,j,k,l,NUM)       
                        c=False
            print(k)
            k00+=1    
            
    def tryval(self,i,j,k,l,NUM):
        global Dname
        k00=0
        Dname[NUM]=Sud()
        lpossible=self.possibles[(i,j,k,l)]
 
        c=1
        for elem in lpossible:
            
            k00+=1
            Dname[NUM].tab=deepcopy(self.tab)
            Dname[NUM].possibles=dict.copy(self.possibles)
            Dname[NUM].tab[i,j,k,l]=elem
            Dname[NUM].possibles[(i,j,k,l)]=[elem]
            
            self.text[i,j,k,l].set_text(str(elem))
            self.text[i,j,k,l].set_color('r')
            c=1
            print(NUM,lpossible,Dname[NUM].possibles[(i,j,k,l)], i,j,k,l)

            while c==1:
                c=Dname[NUM].updatedicassume()
            plt.pause(0.1)
            
            if c==0:
                lzero=Dname[NUM].zero()
                if lzero==[]:
                    return True
                else:
                    if Dname[NUM].assume(lzero,(10+NUM+k00)):
                        return True
                    else:
                        Dname[NUM].delete()
                        c=2
                        # return False
                        
                            
                            


        Dname[NUM].delete()

        return False
        
                        
                        
                
        

# a.tab[0,0]=np.array([[ 0, 0,  1],
#        [ 6,  0,  0],
#        [ 4,  0,  2]])
# a.tab[0,1]=np.array([[ 0,  0,  0.],
#        [ 1,  7, 0],
#        [ 0,  0,  0]])
# a.tab[0,2]=np.array([[ 0,  0,  6],
#        [ 8,  0,  0],
#        [ 5,  7,  1]])
# a.tab[1,0]=np.array([[ 0,  0,  8],
#        [ 0,  0.,  0],
#        [ 0,  4, 0]])
# a.tab[1,1]=np.array([[ 4,  0,  3],
#        [ 0,  0,  0],
#        [ 5,  0,  9]])
# a.tab[1,2]=np.array([[ 0,  5,  0],
#        [ 0,  0.,  0],
#        [ 6,  0,  0]])
# a.tab[2,0]=np.array([[ 1,  2,  6],
#        [ 0, 0,  5],
#        [ 8,  0,  0]])
# a.tab[2,1]=np.array([[ 0,  0,  0],
#        [ 0,  9,  4],
#        [ 0.,  0,  0]])
# a.tab[2,2]=np.array([[ 9,  0,  5],
#        [ 0, 0,  2],
#        [ 7,  0,  0]])
# 

# 
# a.tab[0,0]=np.array([[ 0, 0,  0],
#        [ 0,  0,  0],
#        [ 0,  0,  0]])
# a.tab[0,1]=np.array([[ 0,  0,  0.],
#        [ 7,  8, 0],
#        [ 0,  0,  0]])
# a.tab[0,2]=np.array([[ 0,  0,  0],
#        [ 0,  0,  3],
#        [ 9,  0,  7]])
# a.tab[1,0]=np.array([[ 0,  0,  3],
#        [ 0,  0.,  0],
#        [ 0,  9, 0]])
# a.tab[1,1]=np.array([[ 0,  5,  7],
#        [ 0,  2,  0],
#        [ 0,  0,  0]])
# a.tab[1,2]=np.array([[ 1,  0,  8],
#        [ 0,  7.,  0],
#        [ 0,  0,  5]])
# a.tab[2,0]=np.array([[ 0,  1, 0],
#        [ 0, 2,  0],
#        [ 0,  0,  8]])
# a.tab[2,1]=np.array([[ 0,  0,  2],
#        [ 0,  7,  6],
#        [ 0.,  3,  5]])
# a.tab[2,2]=np.array([[ 0,  0,  6],
#        [ 5, 8,  0],
#        [ 7,  0,  9]])

# 
a=Sud()      
a.tab[0,0]=np.array([[ 0, 0,  6],
       [ 0,  9,  0],
       [ 3,  0,  0]])
a.tab[0,1]=np.array([[ 0,  0,  1],
       [ 0,  3, 0],
       [ 6,  0,  0]])
a.tab[0,2]=np.array([[ 0,  0,  5],
       [ 0,  2,  0],
       [ 8,  0, 0]])
a.tab[1,0]=np.array([[ 6,  0,  0],
       [ 0,  8,  0],
       [ 0,  0, 7]])
a.tab[1,1]=np.array([[ 4,  0,  0],
       [ 0,  6,  0],
       [ 0,  0,  3]])
a.tab[1,2]=np.array([[ 2,  0,  0],
       [ 0,  5,  0],
       [ 0,  0,  9]])
a.tab[2,0]=np.array([[ 0,  0, 3],
       [ 0, 2,  0],
       [ 4,  0,  0]])
a.tab[2,1]=np.array([[ 0,  0,  8],
       [ 0,  9,  0],
       [ 3,  0,  0]])
a.tab[2,2]=np.array([[ 0,  0,  6],
       [ 0, 4,  0],
       [ 5,  0,  0]])
       
a.remplissage()

def sudoku(): #REMPLIR CASE PAR CASE
    a=Sud()
    for i in range(3):
        for j in range(3):
            l = list(map(int, input().split()))
            # print(l)
            a.tab[i,j]=np.array([l[:3],l[3:6],l[6:]])
    return a
