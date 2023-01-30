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
import matplotlib.pyplot as plt
from src.solver.initial_greedy import *
class Simulatedannealing:
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
    
    def greedy(self):
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
        # a=np.ones(num_trucks,)
        # print(f"Number of goods delivered: {int(matrix.sum())}/{self.num_customers}")
        # print(f"Total goods' values: {(value@matrix)@a}")
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

    def create_neighbour(self,matrix:np,bina):
        self.__read_input()
        num_customers=self.num_customers
        num_trucks=self.num_trucks
        quantity=self.__quantity
        value=self.__value 
        lower_bound=self.__lower_bound
        upper_bound=self.__upper_bound 
        
        while True:
            N=randint(1,num_customers)
            lst=sample(range(num_customers),k=N)
            new_matrix=deepcopy(matrix)
            for customer in lst :
                rd= choice(bina)
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
        
       
    
    def simulated_annealing(self,temperature:int, cooling_rate:float, timelimit:int):
        self.__read_input()
        num_customers=self.num_customers
        num_trucks=self.num_trucks
        quantity=self.__quantity
        value=self.__value 
        start= time.time()
        current_temperature = temperature
        
        # greedy_solution = self.greedy()
        greedy_solution = GreedySolver(input_file=self.__input_file).solve().T
        
        initial_solution = self.create_neighbour(greedy_solution,self.create_binary())
        
        current_solution = initial_solution
        current_score = self.objective_function(initial_solution)
        
        best_solution = current_solution
        best_score = current_score
        
        n=1
        record_score=[current_score]
        
        while True:
            for t in range (999999999):
                
                end=time.time() 
                if end - start >= timelimit:
                    # print(f'best_value = {int(best_score)}/{value.sum()}, total packages = {int(best_solution.sum())}/{num_customers}')
                    # plt.plot(record_score)
                    # plt.show()
                    return best_solution,best_score
                
                # find randomly neighbors / current solution for solution
                next_solution=self.create_neighbour(current_solution,self.create_binary())
                next_score = self.objective_function(next_solution)
            
                E = next_score - current_score
                EA=abs(E)

                if E < 0:
                    if EA==0:
                        continue
                    
                    p = exp(E/(EA*current_temperature)) 
                    # decision to accept the worse solution or not 
                    if random()<p: #random() is probability in this case
                        accept = True # this worse solution is accepted
                    else:
                        accept = False # this worse solution is not accepted
                else:
                    accept = True # accent better solution
                     
                if accept==True:
                    current_score = next_score
                    current_solution = next_solution # update the best solution
                    n = n + 1 # count the solutions accepted
                    EA = (EA *(n-1) + E)/n # update EA by chosen formula
                record_score.append(current_score)
                current_temperature = current_temperature*cooling_rate
                
                if best_score <= current_score:
                    best_solution = current_solution
                    best_score = current_score
    def solve(self):
        self.__read_input()

        self.solution,self.objective_value = self.simulated_annealing(temperature=1000,cooling_rate=0.7,timelimit=60)      
        self.num_deliver_packages = self.solution.sum()            
if __name__ =="__main__":
    
    t1=time.time()
    solver=Simulatedannealing(input_file='1.txt')
    print(solver.objective_function(solver.create_neighbour(solver.greedy(),solver.create_binary())))
    solver.simulated_annealing(temperature=1000,cooling_rate=0.7,timelimit=60)
    t2=time.time()
    print(t2-t1)

                    
                    
                    
        







