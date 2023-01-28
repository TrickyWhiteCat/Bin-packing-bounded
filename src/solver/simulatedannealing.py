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

if __name__ == "__main__":
    from greedy import GreedySolver
else:
    from .greedy import GreedySolver

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

    def check_constraints(self, matrix):

        quantity=self.__quantity

        lower_bound=self.__lower_bound
        upper_bound=self.__upper_bound 
        
        real_load_matrix=np.dot(quantity,matrix)

        for i,weight in enumerate(real_load_matrix):
            if  weight > upper_bound[i] or weight < lower_bound[i]:
                return False
        return True
    
    def create_initial_state(self):
        greedy_solver = GreedySolver(input_file=self.__input_file)
        return greedy_solver.solve().T
    
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
        
        K=np.ones(self.num_trucks,)
        return (self.__value@matrix)@K
         
       
    
    def simulated_annealing(self,matrix:np):

        # Customization section:
        initial_temperature = 100
        cooling = 0.7  # cooling coefficient
        computing_time = 10 # second(s)

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

        for t in range(9999999):
            for attempt in range(no_attempts):    
                
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
                    accept= True # accent better solution

                if accept:
                    best_solution = current_solution # update the best solution
                    best_fitness = self.objective_function(best_solution)
                    n = n + 1 # count the solutions accepted
                    EA = (EA *(n-1) + E)/n # update EA by chosen formula

            print('interation: {}, best_fitness: {}'.format(t, best_fitness), end="\r")
           
            record_best_fitness.append(best_fitness)
            # cooling the temperature
            current_temperature = current_temperature*cooling
            
            
        # compute time
            end =time.time()
            if end-start >= computing_time:
                break

def main():
    t1=time.time()
    solver=Solver(input_file='1.txt')
    ma=solver.create_initial_state()

    mm=solver.simulated_annealing(ma)

    t2=time.time()
    print(t2-t1)

if __name__ == "__main__":
    main()