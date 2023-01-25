from VarIntLS import VarIntLS
from LocalSearchManager import LocalSearchManager
from NotEqual import NotEqual
from NotEqualFunction import NotEqualFunction
from AllDifferentFunction import AllDifferentFunction
from ConstraintSystem import ConstraintSystem
from PlusVarConst import PlusVarConst
from HillClimbingSearch import HillClimbingSearch
import random as rd

def printSolution():
	table = [[0 for i in range(n)] for j in range(n)]
	for i in range(n):
		table[i][x[i].getValue()] = 1
	for i in range(n):
		info = ''
		for j in range(n):
			info = info + str(table[i][j]) + '  '
		print(info + '\n')

def printStatus():
	for i in range(n):
		print('x[',i,'] = ',x[i].getValue())
	constraints[0].print()
	constraints[1].print()
	constraints[2].print()
	print('---------------\n')
	
n = 200
mgr = LocalSearchManager()
x = [VarIntLS(mgr,0,n-1,0,'x[' + str(i) + ']') for i in range(n)]
constraints = []
f0 = [PlusVarConst(x[i],0,'f0[' + str(i) + ']') for i in range(n)]
f1 = [PlusVarConst(x[i],i,'f1[' + str(i) + ']') for i in range(n)]
f2 = [PlusVarConst(x[i],-i,'f2[' + str(i) + ']') for i in range(n)]

'''
for i in range(n-1):
	for j in range(i+1,n):
		c = NotEqual(x[i],x[j],'NotEqual(' + x[i].name() + ',' + x[j].name() + ')')
		constraints.append(c)
		c1 = NotEqualFunction(f1[i],f1[j],'NotEqual(' + f1[i].name() + ',' + f1[j].name() + ')')
		constraints.append(c1)
		c2 = NotEqualFunction(f2[i],f2[j],'NotEqual(' + f2[i].name() + ',' + f2[j].name() + ')')
		constraints.append(c2)
'''

constraints.append(AllDifferentFunction(f0,'AllDifferentFunction0'))
constraints.append(AllDifferentFunction(f1,'AllDifferentFunction1'))
constraints.append(AllDifferentFunction(f2,'AllDifferentFunction2'))		
		
CS = ConstraintSystem(constraints)
mgr.close()


searcher = HillClimbingSearch(CS)	
searcher.search(100000)

#printSolution()	