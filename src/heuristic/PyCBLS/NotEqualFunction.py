class NotEqualFunction:
	def __init__(self,f1,f2,name):
		if name != None:
			self.__name__ = name
		else:	
			self.__name__ = 'NotEqual'
		self.__f1__ = f1
		self.__f2__ = f2
		
		self.__variables__ = []
		self.__mgr__ = f1.getLocalSearchManager()
		self.__violations__ = 0
		self.__mgr__.postInvariant(self)
		self.__depended__ = set()# set of components that depend on self
		f1.getDependedComponents().add(self)
		f2.getDependedComponents().add(self)
	
		self.__set_variables__ = set()
		for x in f1.getVariables():
			self.__set_variables__.add(x)
		for x in f2.getVariables():
			self.__set_variables__.add(x)
		for x in self.__set_variables__:
			self.__variables__.append(x)
			
	def name(self):
		return self.__name__
		
	def getVariables(self):
		return self.__variables__
		
	def getLocalSearchManager(self):
		return self.__mgr__
		
	def getDependedComponents(self):
		return self.__depended__
		
	def initPropagation(self):
		if self.__f1__.getValue() == self.__f2__.getValue():
			self.__violations__ = 1
		else:
			self.__violations__ = 0;
		#print(self.__name__ + '::initPropagate, violations = ' + str(self.__violations__))
		
	def propagate(self,x):		
		self.initPropagation()
		#print(self.__name__ + '::propagate, violations = ' + str(self.__violations__))
		
	def violations(self):
		return self.__violations__
	
	def getSwapDelta(self,x,y):
		if x.getValue() == y.getValue():
			return 0
		df1 = self.__f1__.getSwapDelta(x,y)
		df2 = self.__f2__.getSwapDelta(x,y)
		nv1 = self.__f1__.getValue() + df1
		nv2 = self.__f2__.getValue() + df2
		new_violations = 0
		if nv1 == nv2:
			new_violations = 1
		return new_violations - self.__violations__
		
		
	def getAssignDelta(self,x,v):
		if x.getValue() == v:
			return 0
		df1 = self.__f1__.getAssignDelta(x,v)
		df2 = self.__f2__.getAssignDelta(x,v)
		nv1 = self.__f1__.getValue() + df1
		nv2 = self.__f2__.getValue() + df2
		new_violations = 0
		if nv1 == nv2:
			new_violations = 1
		return new_violations - self.__violations__
