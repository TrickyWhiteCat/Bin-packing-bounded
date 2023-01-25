from PyCBLS.VarIntLS import VarIntLS

class LocalSearchManager:
	def __init__(self):
		self.__name__ = 'LocalSearchManager'
		print(self.__name__ + 'constructor')
		self.__map__ = {} # map[x] is the list of topo-sorted depended invariants for propagation
		self.__invariants__ = []
		self.__variables__ = []
		
		
	def postVar(self,var):
		self.__variables__.append(var)
		
	def postInvariant(self,invariant):
		self.__invariants__.append(invariant)
			
	def getInvariants(self):
		return self.__invariants__
		
	def getVariables(self):
		return self.__variables__
		
	def propagate(self,x):
		#print(self.__name__,'::propagate(',x.name(),')')
		for i in self.__map__[x]:
			i.propagate(x)
			
		return	
	
	def topoSortInvariants(self):
		# topo sort invariants for propagation
		self.__topoList__ = []
		
		d = {}
		for i in self.__variables__:
			d[i] = 0
		for i in self.__invariants__:
			d[i] = 0
		
		for i in self.__variables__:
			for j in i.getDependedComponents():
				d[j] = d[j] + 1
				#print('topoSortInvariants, from variables ' + i.name() + ': d[' + j.name() + '] = ' + str(d[j]))
				
		for i in self.__invariants__:
			for j in i.getDependedComponents():
				d[j] = d[j] + 1
				#print('topoSortInvariants, from invariants ' + i.name() + ': d[' + j.name() + '] = ' + str(d[j]))
				
		Q = []
		for i in self.__variables__:
			if d[i] == 0:# consider only invariants
				Q.append(i)
				#print('topoSortInvariants, init Q.push(' + i.name() + ')')
				
		while len(Q) > 0:
			i = Q.pop(0)
			#if not isinstance(i,VarIntLS):
			self.__topoList__.append(i)
			#print('TOPOLIST ADD ' + i.name())
				
			for j in i.getDependedComponents():# arc (i,j)
				#print('POP ',i.name(),' depended ',j.name(),' d = ',d[j])
				d[j] = d[j] - 1
				if d[j] == 0:
					Q.append(j)
		
		print('topoSortInvariants finished')
		
	def getTopoSortedDependedComponents(self,x):
		#return the topo sorted list of components that depend on x
		return self.__map__[x]
		
	def buildDepedencyGraph(self,x):
		mark = {}
		for i in self.__invariants__:
			mark[i] = False
		V = set()
		Q = []
		Q.append(x)
		#V.add(x)
		mark[x] = True	
		while len(Q) > 0:
			y = Q.pop(0)
			V.add(y)
			#print('compute V, POP ',y.name())
			
			for i in y.getDependedComponents():# get components that depend on y
				if mark[i] == False:
					Q.append(i)
					mark[i] = True
					#print('compute V, PUSH ',i.name())
					
		#info = ''
		#for i in V:
		#	info = info + i.name() + ','
		#print('V = ',info)
			
		self.__map__[x] = []# list of component sorted by topo, used when propagation
		Q = [] #queue for topo sort
		d = {}
		for i in V:
			d[i] = 0
		#for i in x.getDependedComponents():
		#	if i in V:	
		#		d[i] = d[i] + 1
				
		for i in V:
			for j in i.getDependedComponents():# arc (i,j): j depends on i
				d[j] = d[j] + 1
				#print('d[',j.name(),' = ',d[j])
				
		#for i in x.getDependedComponents():
		for i in V:
			if True:#i != x:
				#print('d[' + i.name() + '] = ',d[i])
				#if d[i] == 1 or d[i] == 0:
				if d[i] == 0:
					Q.append(i)
					#print('Init PUSH',i.name())
					
		while len(Q) > 0:
			i = Q.pop(0)# remove i from the dependency graph
			#print('POP',i.name())
			if i != x:
				self.__map__[x].append(i)#list of topo sorted  invariants, used when propagation
				
			for j in i.getDependedComponents():# arc (i,j)
				#print('POP ',i.name(),' depended ',j.name(),' d = ',d[j])
				d[j] = d[j] - 1
				if d[j] == 0:
					Q.append(j)
					#print('PUSH',j.name())
		'''				
		print('for variable ',x.name(),' topo-sorted list = ')
		for i in self.__map__[x]:
			print(i.name())
		print('--------------')
		'''
	def close(self):
		print(self.__name__ + '::close')
		'''
		for x in self.__variables__:
			print('depended ',x.name(),' = ')
			for i in x.getDependedComponents():
				print(i.name())
		
		for i in self.__invariants__:
			print('depedned ',i.name(),' = ')
			for j in i.getDependedComponents():
				print(j.name())
		print('---------------')
		'''
		
		
		for x in self.__variables__:
			self.buildDepedencyGraph(x)	
			#break
		
		self.topoSortInvariants()
		
		for i in self.__topoList__:
			i.initPropagation()
		
		
		'''		
		for e in range(5):
			queue.append(e)
		while len(queue) > 0:
			e = queue.pop(0)
			print(e)
		'''