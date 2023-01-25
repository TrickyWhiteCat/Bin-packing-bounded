class NotEqual:
	def __init__(self,x,y,name):
		if name != None:
			self.__name__ = name
		else:	
			self.__name__ = 'NotEqual'
		self.__x__ = x
		self.__y__ = y
		self.__variables__ = [x,y]
		self.__mgr__ = x.getLocalSearchManager()
		self.__violations__ = 0
		self.__mgr__.postInvariant(self)
		self.__depended__ = set()# set of components that depend on self
		x.getDependedComponents().add(self)
		y.getDependedComponents().add(self)
	
	def name(self):
		return self.__name__
		
	def getVariables(self):
		return self.__variables__
		
	def getLocalSearchManager(self):
		return self.__mgr__
		
	def getDependedComponents(self):
		return self.__depended__
		
	def initPropagation(self):
		if self.__x__.getValue() == self.__y__.getValue():
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
		if self.__x__ == x and self.__y__ == y or self.__x__ == y and self.__y__ == x:
			return 0
		if self.__x__ == x or self.__y__ == x:
			return self.getAssignDelta(x,y.getValue())
		elif self.__x__ == y or self.__y__ == y:
			return self.getAssignDelta(y,x.getValue())
		
		return 0
		
	def getAssignDelta(self,x,v):
		#TODO
		if self.__x__ == x:
			newV = 0
			if self.__y__.getValue() == v:
				newV = 1
			return newV - self.__violations__
		elif self.__y__ == x:
			newV = 0
			if self.__x__.getValue() == v:
				newV = 1
			return newV - self.__violations__
			
		return 0;