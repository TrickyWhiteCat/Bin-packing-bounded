'''1. initial state satisfying constraints
2. generate all neighbors satisfying constraints
3. select neighbor by heuristic function (greedy: objective function )
4. Stop if reach maximum iterations or < obj func before
'''
import numpy as np
from random import *
def CreatDataModel(filename,N,K,MaxQ,MinC,MaxC):
    f = open(filename,'w')
    f.write(str(N)+' '+str(K)+'\n')

    D = [randint(1,MaxQ)*10 for i in range(N)]
    C = [randint(MinC,MaxC) for i in range(N)]

    for i in range(N):
        f.write(str(D[i])+' '+str(C[i])+'\n')
    
    x = [randint(0,K) for i in range(N)]
    # The Order i is transported by Truck x[i]

    load = [0 for i in range(K)]
    c1 = [0 for i in range(K)]
    c2 = [0 for i in range(K)]
    
    for k in range(K):
        for i in range(N):
            if x[i] == k:
                load[k] = load[k] + D[i] # The minimal load for truck k
        c1[k] = load[k]
        c2[k] = c1[k] + randint(0,40)

    for k in range(K):
        f.write(str(c1[k])+' '+str(c2[k])+'\n')

def Input(filename):
    with open(filename,'r') as f:
        N,K = list(map(int,f.readline().split()))
        D = []
        C = []
        # lst1 = []
        for i in range(N):
            line = f.readline().split()
            D.append(int(line[0]))
            C.append(int(line[1]))

        c1 = []
        c2 = []
        for k in range(K):
            load = f.readline().split()
            c1.append(int(load[0]))
            c2.append(int(load[1]))

        # print(lst1)

    return N,K,D,C,c1,c2
class Solver:
    def __init__(self,input_file,*args):
        super().__init__(*args)
        self.__input_file=input_file
    def __read_input(self):
        if self.__input_file is None:
            raise(f"No input file was specified!")
        try:
            with open(self.__input_file, "r") as inp_file:
                lines = inp_file.readlines()
        except FileNotFoundError:
            raise(FileNotFoundError(f"File {self.__input_file} is invalid!"))
        quantity=[]
        value=[]
        lower_bound=[]
        upper_bound=[]
        
        #first line
        customers, trucks=[int(val) for val in lines[0].split(' ')]

        ## The next N customers lines
        for line in lines[1: customers + 1]:
            q, v = [int(val) for val in line.split(" ")]
            quantity.append(q)
            value.append(v)
        ## The last K trucks lines
        for line in lines[-trucks:]:
            low, high = [int(val) for val in line.split(" ")]
            lower_bound.append(low)
            upper_bound.append(high)
        # store arguments as attributes
        self.num_customers = customers
        self.num_trucks = trucks
        
        self.__quantity = np.array(quantity)
        self.__value = np.array(value)
        self.total_value = sum(value)

        self.__lower_bound = lower_bound
        self.__upper_bound = upper_bound
    def create_constraints(self, matrix:np):
        self.__read_input()
        num_customers=self.num_customers
        num_trucks=self.num_trucks

        quantity=self.__quantity
        value=self.__value 
        total_value=self.total_value

        lower_bound=self.__lower_bound
        upper_bound=self.__upper_bound 
        
        real_weight_matrix=np.dot(quantity,matrix)
        print(real_weight_matrix)
        for i,weight in enumerate(real_weight_matrix):
            if  weight > upper_bound[i] or weight < lower_bound[i]:
                return False
        return True
        # for truck in range(num_trucks):
        #     sum=0
        #     for customer in 
        
        
    
    def create_initial_state(self):
        self.__read_input()
        num_customers=self.num_customers
        num_trucks=self.num_trucks

        quantity=self.__quantity
        value=self.__value 
        total_value=self.total_value

        lower_bound=self.__lower_bound
        upper_bound=self.__upper_bound 
        
        customer_rate=[(i,value[i]/quantity[i]) for i in range(num_customers)]
        customer_rate.sort(key=lambda x: -x[1])
        truck_rate=[(i,upper_bound[i]) for i in range(num_trucks)]
        truck_rate.sort(key=lambda x: -x[1])
        print(customer_rate)
        matrix=np.zeros((num_customers,num_trucks))
        
        real_weight=[0 for truck in range(num_trucks)]
        
        for pair in customer_rate:
            r=pair[0]
            q_customer=quantity[r]
            v_customer=value[r]
            
            for t in truck_rate:
                truck=t[0]
                lower=lower_bound[truck]
                upper=upper_bound[truck]
                
                if q_customer <= lower or lower <= q_customer <= upper:
                    if real_weight[truck] <= lower or lower <= real_weight[truck] <=upper :
                        real_weight[truck] +=q_customer
                        matrix[r][truck]=1
                        if  lower <= real_weight[truck] <=upper:
                            break
                        if real_weight[truck] <= lower:
                                break
                        else: 
                            real_weight[truck]-=q_customer
                            matrix[r][truck]=0
        
        # s=sum([value[i] for i in range(num_customers) if matrix[i][:].sum() ])
        
        return matrix
    
    
solver=Solver(input_file='1.txt')
ma=solver.create_initial_state()
d=solver.create_constraints(ma)
print(d)
   
                    
                    
                    
        







