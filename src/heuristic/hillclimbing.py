'''1. initial state satisfying constraints
2. generate all neighbors satisfying constraints
3. select neighbor by heuristic function (greedy: objective function )
4. Stop if reach maximum iterations or < obj func before
'''
import time
import numpy as np
from random import *
from copy import deepcopy
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

    def check_constraints(self, matrix:np):
        self.__read_input()
        num_customers=self.num_customers
        num_trucks=self.num_trucks

        quantity=self.__quantity
        value=self.__value 
        total_value=self.total_value

        lower_bound=self.__lower_bound
        upper_bound=self.__upper_bound 
        
        real_load_matrix=np.dot(quantity,matrix)
        #print(real_load_matrix)
        for i,weight in enumerate(real_load_matrix):
            if  weight > upper_bound[i] or weight < lower_bound[i]:
                return False
        return True
    
    def create_initial_state(self):
        self.__read_input()

        num_customers=self.num_customers
        num_trucks=self.num_trucks

        quantity=self.__quantity
        value=self.__value 
        total_value=self.total_value

        lower_bound=self.__lower_bound
        upper_bound=self.__upper_bound 
        
        customer_rate=[(i, value[i]) for i in range(num_customers)]
        customer_rate.sort(key=lambda x: -x[1]) # Sort giam dan

        truck_rate=[(i,upper_bound[i]) for i in range(num_trucks)]
        truck_rate.sort(key=lambda x: -x[1])

        matrix=np.zeros((num_customers,num_trucks))
        
        real_load=[0 for truck in range(num_trucks)]
        
        for idx, rate in customer_rate:

            q_customer=quantity[idx]
            v_customer=value[idx]
            
            # Nhet du lower
            for t in truck_rate: # Chon xe
                truck=t[0]
                lower=lower_bound[truck]
                upper=upper_bound[truck]

                if real_load[truck] < lower and real_load[truck] + q_customer <= upper: # nhet du lower da
                    real_load[truck] += q_customer
                    matrix[idx][truck]=1
                    break

        # Toi day la co du lower bound r, phai check xem hang dc nhet vao xe chua, chua dc nhet thi minh nhet vao
        for idx, rate in customer_rate:
            if matrix[idx].sum() > 0:
                continue
            q_customer=quantity[idx]
            
            # Nhet du lower
            #print(f"{q_customer=}")
            for t in truck_rate: # Chon xe
                truck=t[0]
                lower=lower_bound[truck]
                upper=upper_bound[truck]

                #print(f"Truck {truck} load: {real_load[truck]}, upper bound: {upper}, diff: {upper - real_load[truck]}")
                if real_load[truck] + q_customer <= upper: # nhet vua xe
                    real_load[truck] += q_customer
                    matrix[idx][truck]=1
                    break
        a=np.ones(num_trucks,)
        print(f"Number of goods delivered: {int(matrix.sum())}/{self.num_customers}")
        print(f"Total goods' values: {(value@matrix)@a}")
        
        return matrix
    
    def create_binary(self):
        self.__read_input()
        num_trucks=self.num_trucks
        a=[0]*num_trucks
        lst=[a[:]]
        for i in range(num_trucks):
            b=a[:]
            a[i]=1
            lst.append(a)
            a=b
        return lst

    def create_neighbour(self,matrix:np): #dynamic neighbourhood size
        self.__read_input()
        num_customers=self.num_customers
        num_trucks=self.num_trucks
        quantity=self.__quantity
        value=self.__value 
        lower_bound=self.__lower_bound
        upper_bound=self.__upper_bound 
        bina=self.create_binary()
        while True:
            N=randint(1,num_customers)
            lst=sample(range(num_customers),k=N)
            for customer in lst :
                matrix[customer] = choice(bina)
            return matrix
        
    def fitness(self,matrix:np):
        if self.check_constraints(matrix):
            return self.objective_function(matrix)
        return 0
    
    def objective_function(self,matrix:np):
        self.__read_input()
        num_customers=self.num_customers
        num_trucks=self.num_trucks
        quantity=self.__quantity
        value=self.__value 
        lower_bound=self.__lower_bound
        upper_bound=self.__upper_bound
        
        K=np.ones(num_trucks,)
        return (value@matrix)@K
    
    def hill_climbing(self,matrix:np):
        if not self.check_constraints(matrix):
            return 
        initial_solution=matrix
        current_solution=initial_solution
        best_fitness=self.fitness(matrix)
        t1=time.time()
        for k in range(1000):
            while True:
                current_solution = self.create_neighbour(current_solution)
                temp=self.fitness(current_solution)
                if best_fitness < temp:
                    best_fitness=temp
                    break
                t2=time.time()
                if t2-t1 >= 60:
                    return 
            print(k,f'best_fitness={best_fitness}')
        
        
t1=time.time()
solver=Solver(input_file='1.txt')
ma=solver.create_initial_state()
# d=solver.create_constraints(ma)
# d=solver.create_binary()
# mm=solver.create_neighbors(ma)
hill=solver.hill_climbing(ma)
# print(ma)
t2=time.time()
print(t2-t1)
   
                    
                    
                    
        








