class LessOrEqualFunctionConst:
	def __init__(self,f,v,name):
		if name != None:
			self.__name__ = name
		else:	
			self.__name__ = 'NotEqual'
		self.__f__ = f
		self.__v__ = v
		
		self.__variables__ = f.getVariables()
		self.__mgr__ = f.getLocalSearchManager()
		self.__violations__ = 0
		self.__mgr__.postInvariant(self)
		self.__depended__ = set()# set of components that depend on self
		f.getDependedComponents().add(self)
		
		
			
	def name(self):
		return self.__name__
		
	def getVariables(self):
		return self.__variables__
		
	def getLocalSearchManager(self):
		return self.__mgr__
		
	def getDependedComponents(self):
		return self.__depended__
		
	def initPropagation(self):
		if self.__f__.getValue() <= self.__v__:
			self.__violations__ = 0
		else:
			self.__violations__ = self.__f__.getValue() - self.__v__
			
		#print(self.__name__ + '::initPropagate, violations = ' + str(self.__violations__))
		
	def propagate(self,x):		
		self.initPropagation()
		#print(self.__name__ + '::propagate, violations = ' + str(self.__violations__))
		
	def violations(self):
		return self.__violations__
	
	def getSwapDelta(self,x,y):
		if x.getValue() == y.getValue():
			return 0
		df = self.__f__.getSwapDelta(x,y)
		nv = self.__f__.getValue() + df
		new_violations = 0
		if nv > self.__v__:
			new_violations = nv - self.__v__
			
		return new_violations - self.__violations__
		
		
	def getAssignDelta(self,x,v):
		if x.getValue() == v:
			return 0
		df = self.__f__.getAssignDelta(x,v)
		nv = self.__f__.getValue() + df
		new_violations = 0
		if nv > self.__v__:
			new_violations = nv - self.__v__
			
		return new_violations - self.__violations__
