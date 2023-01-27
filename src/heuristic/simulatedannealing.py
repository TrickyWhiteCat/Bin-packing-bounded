'''1. initial state satisfying constraints
2. generate all neighbors satisfying constraints
3. select neighbor by heuristic function (greedy: objective function )
4. Stop if reach maximum iterations or < obj func before
'''
import time
import numpy as np
from random import *
from copy import deepcopy
from math import *
import matplotlib  as plt
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
        # matrix[0]=[1,0]
        
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

    def create_neighbour(self,matrix:np):
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
            # for N in range(num_customers):
            lst=sample(range(num_customers),k=N)
            new_matrix=deepcopy(matrix)
            for customer in lst :
                rd= choice(bina)
                # if new_matrix[customer] != rd:
                new_matrix[customer] = rd
            if self.check_constraints(new_matrix) and (not (new_matrix==matrix).all()) :
                break
        return new_matrix
    

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
         
       
    
    def simulated_annealing(self,matrix:np):
        
        import matplotlib.pyplot as plt
        # Customization section:
        initial_temperature = 100
        cooling = 0.7  # cooling coefficient
        number_variables = 2
        computing_time = 120 # second(s)
        # Simulated Annealing Algorithm:
        initial_solution=matrix
        current_solution = initial_solution
        best_solution = initial_solution
        n = 1  # no of solutions accepted
        best_fitness = self.objective_function(best_solution)
        current_temperature = initial_temperature # current temperature
        start = time.time()
        no_attempts = 100 # number of attempts in each level of temperature
        record_best_fitness=[]

        for t in range (9999999) :
            print(t)
            for attemp in range(no_attempts):    
                
            # find randomly neighbors/current solution for solution
                current_solution=self.create_neighbour(current_solution)
                
                current_fitness = self.objective_function(current_solution)
                E = abs(current_fitness - best_fitness)
                if t == 0 :
                    EA=E
                #schedule(t) is EA*
                if current_fitness < best_fitness:
                    p = exp(-E/(EA*current_temperature)) #T high p high 
            # decision to accept the worse solution or not 
                    if random()<p: #random() is probability in this case
                        accept = True # this worse solution is accepted
                    else:
                        accept = False # this worse solution is not accepted
                else:
                    accept=  True # accent better solution 
                if accept==True:
                    best_solution = current_solution # update the best solution
                    best_fitness = self.objective_function(best_solution)
                    n = n + 1 # count the solutions accepted
                    EA = (EA *(n-1) + E)/n # update EA by chosen formula
            print ('interation: {}, best_fitness: {}'.format(t, best_fitness))
           
            record_best_fitness.append(best_fitness)
            # cooling the temperoture
            current_temperature = current_temperature*cooling
            
            
        # compute time
            end =time.time ()
            if end-start >= computing_time:
                break
        plt.plot(record_best_fitness)
        plt.show()

       
              
        
   
        
        
        
        
t1=time.time()
solver=Solver(input_file='1.txt')
ma=solver.create_initial_state()

mm=solver.simulated_annealing(ma)

t2=time.time()
print(t2-t1)
   
                    
                    
                    
        








