'''1. initial state satisfying constraints
2. generate all neighbors satisfying constraints
3. select neighbor by heuristic function (greedy: objective function )
4. Stop if reach maximum iterations or < obj func before
'''
import time
import numpy as np
from random import *
from copy import deepcopy
if __name__ == "__main__":
    from utils.initial_greedy import GreedySolver
else:
    from .utils.initial_greedy import GreedySolver

class HillClimbing:
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

        quantity=self.__quantity

        lower_bound=self.__lower_bound
        upper_bound=self.__upper_bound 
        
        real_load_matrix=np.dot(quantity,matrix)
        for i,weight in enumerate(real_load_matrix):
            if  weight > upper_bound[i] or weight < lower_bound[i]:
                return False
        return True
    
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
        num_trucks=self.num_trucks
        value=self.__value
        
        K=np.ones(num_trucks,)
        return (value@matrix)@K
    
    def hill_climbing(self,timelimit):
        self.__read_input()
        start = time.time()
        
        
        greedy_solution = GreedySolver(input_file=self.__input_file).solve().T
        initial_solution= self.create_neighbour(greedy_solution)
    
        current_solution = initial_solution
        current_score = self.objective_function(initial_solution)
        
        best_solution = current_solution
        best_score = current_score
        record_score =[current_score]
        
        while True:
            end=time.time() 
            if end - start >= timelimit:
                return best_solution,best_score
            next_solution = self.create_neighbour(current_solution)
            next_score = self.objective_function(next_solution)

            if best_score <= next_score:
                best_solution = next_solution
                best_score = next_score
                record_score.append(best_score)
            else:
                current_solution= next_solution

    def solve(self,timelimit=60):
        self.__read_input()
        
        self.solution,self.objective_value = self.hill_climbing(timelimit)      
        
        self.solution,self.objective_value = self.hill_climbing(timelimit)      
        self.num_deliver_packages = self.solution.sum()
        
        return self.solution
    
    def plan(self,timelimit = 60):
        self.solution = self.solve(timelimit=timelimit)
        if self.solution is None:
            return f"No solution found"
        plan = []
        for weight in self.solution.T:
            on_this_truck = []
            for index, elem in enumerate(weight):
                if elem == 1:
                    on_this_truck.append(index + 1)
            plan.append(on_this_truck)

        string_plan = "\n\n".join([f"- Truck {idx+1} contains goods of {len(plan[idx])} customers: {', '.join([str(val) for val in on_this_truck])}" for idx, on_this_truck in enumerate(plan)])
        res = f"With the maximum total values of {int(self.objective_value)}/{self.total_value}, we deliver {self.num_deliver_packages}/{self.num_customers} packages with the plan below: \n{string_plan}"
        return res      
        
if __name__ =="__main__":     
          
    solver=HillClimbing(input_file='data.txt')
    print(solver.plan())