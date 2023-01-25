from PyCBLS.VarIntLS import VarIntLS
from PyCBLS.LocalSearchManager import LocalSearchManager
from PyCBLS.NotEqual import NotEqual
from PyCBLS.NotEqualFunction import NotEqualFunction
from PyCBLS.AllDifferentFunction import AllDifferentFunction
from PyCBLS.ConstraintSystem import ConstraintSystem
from PyCBLS.PlusVarConst import PlusVarConst
from PyCBLS.LessOrEqualFunctionConst import LessOrEqualFunctionConst
from PyCBLS.HillClimbingSearch import HillClimbingSearch
from random import *
def CreatDataModel(filename,N,K,MaxQ,MinC,MaxC):
    f = open(filename,'w')
    f.write(str(N)+' '+str(K)+'\n')

    D = [randint(1,MaxQ)*10 for i in range(N)]
    C = [randint(MinC,MaxC) for i in range(N)]

    for i in range(N):
        f.write(str(D[i])+' '+str(C[i])+'\n')
    
    x = [randint(0,K) for i in range(N)]
    # The Order i is transported by Truck x[i]

    load = [0 for i in range(K)]
    c1 = [0 for i in range(K)]
    c2 = [0 for i in range(K)]
    
    for k in range(K):
        for i in range(N):
            if x[i] == k:
                load[k] = load[k] + D[i] # The minimal load for truck k
        c1[k] = load[k]
        c2[k] = c1[k] + randint(0,40)

    for k in range(K):
        f.write(str(c1[k])+' '+str(c2[k])+'\n')

def Input(filename):
    with open(filename,'r') as f:
        N,K = list(map(int,f.readline().split()))
        D = []
        C = []
        # lst1 = []
        for i in range(N):
            line = f.readline().split()
            D.append(int(line[0]))
            C.append(int(line[1]))

        c1 = []
        c2 = []
        for k in range(K):
            load = f.readline().split()
            c1.append(int(load[0]))
            c2.append(int(load[1]))

        # print(lst1)

    return N,K,D,C,c1,c2
def main(inputfile:tuple):
    N,K,weight,value,w1,w2=inputfile
    mgr=LocalSearchManager()
    
    x=[[VarIntLS(mgr,0,1,0,f'x[{customer}][{truck}]') for truck in range(K)] for customer in range(N)]
    
    #constraint
    constraints=[]
    f0=[sum([x[customer][truck].getValue() for truck in range(K)]) for customer in range(N)]
    f1=[sum([x[customer][truck].getValue() for customer in range(N)]) for truck in range(K)]
    f2=[-sum([x[customer][truck].getValue() for customer in range(N)]) for truck in range(K)]
    
    constraints.append(LessOrEqualFunctionConst(f0,1,'customer1truck'))
    constraints.append(LessOrEqualFunctionConst(f1,w2,'upperbound'))
    constraints.append(LessOrEqualFunctionConst(f2,-w1,'lowerbound'))
    
    CS=ConstraintSystem(constraints)
    mgr.close()
    searcher=HillClimbingSearch(CS)
    searcher.search(10000)
if __name__=='__main__':
    inputfile=Input('1.txt')
    main(inputfile)
    




