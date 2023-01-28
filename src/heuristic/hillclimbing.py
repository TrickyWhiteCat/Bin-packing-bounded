'''1. initial state satisfying constraints
2. generate all neighbors satisfying constraints
3. select neighbor by heuristic function (greedy: objective function )
4. Stop if reach maximum iterations or < obj func before
'''
import time
import numpy as np
from random import *
from copy import deepcopy
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
        # print(f"Number of goods delivered: {int(matrix.sum())}/{self.num_customers}")
        # print(f"Total goods' values: {(value@matrix)@a}")
        
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

    # def create_neighbour(self,matrix:np): #dynamic neighbourhood size
    #     self.__read_input()
    #     num_customers=self.num_customers
    #     num_trucks=self.num_trucks
    #     quantity=self.__quantity
    #     value=self.__value 
    #     lower_bound=self.__lower_bound
    #     upper_bound=self.__upper_bound 
    #     bina=self.create_binary()
    #     while True:
    #         N=randint(1,num_customers)
    #         lst=sample(range(num_customers),k=N)
    #         for customer in lst :
    #             matrix[customer] = choice(bina)
    #         return matrix
    
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
    
    # def hill_climbing(self,matrix:np):
    #     if not self.check_constraints(matrix):
    #         return 
    #     initial_solution=matrix
    #     current_solution=initial_solution
    #     best_fitness=self.fitness(matrix)
    #     feasible_lst=[(matrix,best_fitness)]
    #     t1=time.time()
    #     while True:
    #         current_solution = self.create_neighbour(current_solution)
    #         temp=self.fitness(current_solution)
    #         # print(best_fitness,temp)
    #         if best_fitness <= temp:
    #             best_fitness=temp
    #             print(self.check_constraints(current_solution))
    #             print(temp)
    #             feasible_lst.append((current_solution,self.fitness(current_solution)))
                
    #         t2=time.time()
    #         if t2-t1 >= 5:
    #             feasible_lst.sort(key=lambda x: x[1], reverse=True)
    #             print(feasible_lst)
    #             print(f'best_fitness={feasible_lst[0][1]}, total packages ={feasible_lst[0][0].sum()}', self.check_constraints(feasible_lst[0]))
    #             return 
    def hill_climbing(self,matrix:np):
        if not self.check_constraints(matrix):
            return 
        initial_solution=matrix
        current_solution=initial_solution
        best_fitness=self.objective_function(matrix)
        feasible_lst=[(matrix,best_fitness)]
        t1=time.time()
        while True:
            current_solution = self.create_neighbour(current_solution)
            temp=self.objective_function(current_solution)
            # print(best_fitness,temp)
            if best_fitness <= temp:
                best_fitness=temp
                # print(self.check_constraints(current_solution))
                # print(temp)
                feasible_lst.append((current_solution,self.fitness(current_solution)))
                
            t2=time.time()
            if t2-t1 >= 60:
                feasible_lst.sort(key=lambda x: x[1], reverse=True)
                print(f'best_fitness={feasible_lst[0][1]}, total packages ={feasible_lst[0][0].sum()}', self.check_constraints(feasible_lst[0][0]))
                return 
            
t1=time.time()
solver=Solver(input_file='1.txt')
ma=solver.create_initial_state()
hill=solver.hill_climbing(ma)
t2=time.time()
print(t2-t1)
   
                    
                    
                    
        








