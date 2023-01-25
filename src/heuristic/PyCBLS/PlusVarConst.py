class PlusVarConst:
	def __init__(self,x,v,name):
		if name == None:
			self.__name__ = 'PlusVarConst'
		else:
			self.__name__ = name
		self.__x__ = x
		self.__v__ = v
		self.__mgr__ = x.getLocalSearchManager()
		self.__value__ = 0
		self.__mgr__.postInvariant(self)
		self.__depended__ = set()# set of components that depend on self
		x.getDependedComponents().add(self)
		self.__variables__ = [x]
		
		self.__minValue__ = x.getMinValue() + v
		self.__maxValue__ = x.getMaxValue() + v
		
	
	def name(self):
		return self.__name__
		
	def getVariables(self):
		return self.__variables__
		
	def getLocalSearchManager(self):
		return self.__mgr__
		
	def getDependedComponents(self):
		return self.__depended__
		
	def initPropagation(self):
		self.__value__ = self.__x__.getValue() + self.__v__
		
	def propagate(self,x):
		#print(self.__name__ + '::propagate')
		self.__value__ = self.__x__.getValue() + self.__v__
		
	def getMinValue(self):
		return self.__minValue__
	def getMaxValue(self):
		return self.__maxValue__
		
	def getValue(self):
		return self.__value__

	def getSwapDelta(self,x,y):
		if x == self.__x__:
			return y.getValue() + self.__v__ - self.__value__
		elif y == self.__y__:
			return x.getValue() + self.__v__ - self.__value__
		
		return 0
		
	def getAssignDelta(self,x,v):
		if self.__x__ == x:
			return v + self.__v__ - self.__value__
			
		return 0;
		