from VarIntLS import VarIntLS
from LocalSearchManager import LocalSearchManager
from NotEqual import NotEqual
from ConstraintSystem import ConstraintSystem
from Plus import Plus

mgr = LocalSearchManager()
#n = 10
#X = [VarIntLS(0,mgr,n-1) for i in range(n)]
X1 = VarIntLS(mgr,0,5,'X1')
X2 = VarIntLS(mgr,0,5,'X2')
X3 = VarIntLS(mgr,0,5,'X3')
f1 = Plus(X1,X2,'f1')
f2 = Plus(X2,X3,'f2')
f3 = Plus(X1,X3,'f3')
c1 = NotEqual(f1,f2,'c1')
c2 = NotEqual(f2,f3,'c2')
constraints = []
constraints.append(c1)
constraints.append(c2)
S = ConstraintSystem(constraints)

mgr.close()

print('variables = ',len(mgr.getVariables()))
print('invariants = ',len(mgr.getInvariants()))

X1.setValuePropagate(4)

