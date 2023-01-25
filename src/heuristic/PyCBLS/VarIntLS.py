class VarIntLS:
	def __init__(self,mgr,min,max,name):
		self.__mgr__ = mgr
		self.__min__ = min
		self.__max__ = max
		self.__name__ = name
		self.__value__ = self.__min__
		self.__oldValue__ = min
		self.__mgr__.postVar(self)
		self.__depended__ = set()#set of components that depend on self
		
		#print(self.__name__ + '::constructor')

	def __init__(self,mgr,min,max,init_value,name):
		self.__mgr__ = mgr
		self.__min__ = min
		self.__max__ = max
		self.__name__ = name
		self.__value__ = init_value
		self.__oldValue__ = init_value 
		self.__mgr__.postVar(self)
		self.__depended__ = set()#set of components that depend on self
	
	def name(self):
		return self.__name__
		
	def getLocalSearchManager(self):
		return self.__mgr__
	def getDependedComponents(self):
		return self.__depended__
		
	def getOldValue(self):
		return self.__oldValue__
		
	def getValue(self):
		return self.__value__
	
	def getMinValue(self):
		return self.__min__
		
	def getMaxValue(self):
		return self.__max__

	def initPropagation(self):
		return
		
	def setValuePropagate(self,v):
		self.__oldValue__ = self.__value__
		self.__value__ = v
		self.__mgr__.propagate(self)

	def swapValuePropagate(self,y):
		vy = y.getValue()
		vx = self.getValue()
		self.setValuePropagate(vy)
		y.setValuePropagate(vx)
		