from LocalSearchManager import LocalSearchManager
from VarIntLS import VarIntLS
from NotEqual import NotEqual
from ConstraintSystem import ConstraintSystem
import random as rd

mgr = LocalSearchManager()
x = [[VarIntLS(mgr,1,9,1,'x['+ str(i) + ',' +str(j) + ']') for i in range (9)] for j in range(9)]

def printSolution():
    for i in range(9):
        for j in range(9):
            print(x[i][j].getValue(),end=' ')
        print('')
contraints = []
#contraints on row
for i in range(9):
    for j1 in range(8):
        for j2 in range(j1+1,9):
            c = NotEqual(x[i][j1],x[i][j2],'NotEqual')
            contraints.append(c)

#contraints on col
for i in range(9):
    for j1 in range(8):
        for j2 in range(j1+1,9):
            c = NotEqual(x[j1][i],x[j2][i],'NotEqual')
            contraints.append(c)
#contraints on sub-square

for I in range(3):
    for J in range(3):
        for i1 in range (3):
            for i2 in range(3):
                for j1 in range(3):
                    for j2 in range(3):
                        if i1 != i2 and j1 != j2:
                            c = NotEqual(x[I+3*i1][J+3*j1],x[I+3*i2][J+3*j2],'NotEqual')

C = ConstraintSystem(contraints)

def simpleHillClimbing(maxIters):
    #explore neighborhood for finding the best neighboring solution
    for it in range(maxIters):
        minDelta=1e9
        select_i=-1
        select_j=-1
        select_value=-1
        for i in range(9):
            for j in range(9):
                for v in range(1,10):
                    delta=C.getAssignDelta(x[i][j],v)
                    minDelta=delta
                    select_i=i 
                    select_j=j
                    select_value=v

#perform the selected local move
        x[select_i][select_j].setValuePropagate(select_value)
        print('step',it,'x[',select_i,',',select_j,'] = ',select_value,'violations=',C.violations())




mgr.close() #close the model

#perform local search (hill climbing)
#make use of C.getAssigndelta,C.getSwapDelta for neighborhood query
print('Init, C = ',C.violations())
simpleHillClimbing(1000)
printSolution()
