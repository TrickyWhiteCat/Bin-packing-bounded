import random as rd

class Move:
	def __init__(self,i,v):
		self.i = i
		self.v = v

class HillClimbingSearch:
	def __init__(self, constraint):
		self.__constraint__ = constraint
		self.__variables__ = constraint.getVariables()
		
		
	def search(self,maxIter):
		n = len(self.__variables__)
		x = self.__variables__
		CS = self.__constraint__
		cur = CS.violations()
		
		for iter in range(maxIter):
			cand = []
			minD = 1000000
			for i in range(n):
				for v in range(x[i].getMinValue(), x[i].getMaxValue() + 1):
					d = CS.getAssignDelta(x[i],v)
						#print(iter,': assignDelta(',i,',',v,') = ',d)
					if d < minD:
						cand = []
						cand.append(Move(i,v))
						minD = d
					elif d == minD:
						cand.append(Move(i,v))

			idx = rd.randint(0,len(cand)-1)
			#print(iter,': cand = ',len(cand),' idx = ',idx)
			m = cand[idx]
			x[m.i].setValuePropagate(m.v)
			print(iter,': assign x[',m.i,'] = ',m.v,' violations = ',CS.violations())
			#print(' x = ',[x[i].getValue() for i in range(n)])
			if CS.violations() == 0:
				break
			if cur + minD != CS.violations():
				print('BUG, cur = ',cur,' delta = ',minD,' CS = ',CS.violations())
				break
			cur = CS.violations()	
		