class ConstraintSystem:
	def __init__(self, constraints):
		self.__name__ = 'ConstraintSystem'
		self.__constraints__ = constraints
		self.__set_constraints__ = set()
		self.__violations_of_constraints__ = []
		self.__mapToIndex__ = {}
		print(self.__name__ + '::constructor')
		self.__violations__ = 0
		self.__mgr__ = constraints[0].getLocalSearchManager()
		self.__depended__ = set()
		self.__set_vars__ = set()
		
		for i in range(len(constraints)):
			self.__mapToIndex__[constraints[i]] = i
			self.__violations_of_constraints__.append(0)
			
		for c in constraints:
			c.getDependedComponents().add(self)
			
			self.__set_constraints__.add(c)
			
		for c in constraints:
			for x in c.getVariables():
				self.__set_vars__.add(x)
		self.__variables__ = []
		for x in self.__set_vars__:
			self.__variables__.append(x)
			
		self.__mgr__.postInvariant(self)
	
	#def close(self):
		# construct map[x] the list of topo-sorted components that depend on variable x
		
	def getVariables(self):
		return self.__variables__
		
	def getDependedComponents(self):
		return self.__depended__
		
	def name(self):
		return self.__name__
		
	def initPropagation(self):
		#print(self.__name__ + 'initPropagate')
		#for i in range(len(self.__constraints__)):
		#	self.__constraints__[i].initPropagation()
			
		
		self.__violations__ = 0
		for i in range(len(self.__constraints__)):
			c = self.__constraints__[i]
			self.__violations_of_constraints__[i] = self.__constraints__[i].violations()
			self.__violations__ += self.__constraints__[i].violations()
			

		#print(self.__name__ + '::initPropagate, violations = ' + str(self.__violations__))
		
	def propagate(self,x):
		#print(self.__name__ + '::propagate')
		#for i in range(len(self.__constraints__)):
		#	self.__constraints__[i].initPropagation()

		cx = self.__mgr__.getTopoSortedDependedComponents(x)
		for c in cx:
			if c in self.__set_constraints__:
				idx = self.__mapToIndex__[c]
				# subtract old related violations
				self.__violations__ = self.__violations__ - self.__violations_of_constraints__[idx]
				# add new related violations
				self.__violations__ = self.__violations__ + c.violations()
				self.__violations_of_constraints__[idx] = c.violations()
		
		return
		
		self.__violations__ = 0
		for i in range(len(self.__constraints__)):
			self.__violations__ += self.__constraints__[i].violations()
	
	def getSwapDelta(self,x,y):
		d = 0		
		cx = self.__mgr__.getTopoSortedDependedComponents(x)
		cy = self.__mgr__.getTopoSortedDependedComponents(y)
		
		#for c in self.__constraints__:
		for c in cx:
			if c in self.__set_constraints__:
				d += c.getSwapDelta(x,y)
		for c in cy:
			if c in self.__set_constraints__:
				d += c.getSwapDelta(x,y)
				
		return d	
		
	def getAssignDelta(self,x,v):
		d = 0		
		cx = self.__mgr__.getTopoSortedDependedComponents(x)
		
		#for c in self.__constraints__:
		for c in cx:
			if c in self.__set_constraints__:
				d += c.getAssignDelta(x,v)
				
		return d	
		
	def violations(self):
		return self.__violations__
		