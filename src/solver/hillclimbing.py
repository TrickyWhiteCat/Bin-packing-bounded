'''1. initial state satisfying constraints
2. generate all neighbors satisfying constraints
3. select neighbor by heuristic function (greedy: objective function )
4. Stop if reach maximum iterations or < obj func before
'''
import time
import numpy as np
from random import *


if __name__ == "__main__":
    from greedy import GreedySolver
else:
    from .greedy import GreedySolver

class Solver:
    def __init__(self, input_file, time_limit: int = None, *args):
        super().__init__(*args)
        self.__input_file=input_file
        self.__time_limit = time_limit

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

        lower_bound=self.__lower_bound
        upper_bound=self.__upper_bound 
        
        real_load_matrix=np.dot(self.__quantity,matrix)
        print(real_load_matrix)
        input()
        for i,weight in enumerate(real_load_matrix):
            if  weight > upper_bound[i] or weight < lower_bound[i]:
                return False
        return True
    
    def create_initial_state(self):
        greedy_solver = GreedySolver(input_file=self.__input_file)
        return greedy_solver.solve().T
    
    def create_binary(self):
        num_trucks=self.num_trucks
        a=[0]*num_trucks
        lst=[a[:]]
        for i in range(num_trucks):
            b=a[:]
            a[i]=1
            lst.append(a)
            a=b
        return lst

    def create_neighbour(self,matrix): #dynamic neighbourhood size
        bina=self.create_binary()
        while True:
            N=randint(1,self.num_customers)
            lst=sample(range(self.num_customers),k=N)
            for customer in lst :
                matrix[customer] = choice(bina)
            return matrix
        
    def fitness(self,matrix):
        if self.check_constraints(matrix):
            return self.objective_function(matrix)
        return 0
    
    def objective_function(self,matrix):
        return sum(self.__value@matrix)
    
    def hill_climbing(self,matrix):
        if not self.check_constraints(matrix):
            return

        current_solution=matrix
        best_fitness=self.fitness(current_solution)
        t1=time.time()
        for k in range(1000):
            while True:
                current_solution = self.create_neighbour(current_solution)
                temp=self.fitness(current_solution) # Neu sai constraints thi self.fitness tra ve 0
                if best_fitness < temp: # Suy ra best_fitness luon lon hon temp
                    best_fitness=temp
                    break   # Khong bao gio thoat vong lap
                t2=time.time()
                if self.__time_limit is not None and t2-t1 >= self.__time_limit:
                    return current_solution
            print(k,f'best_fitness={best_fitness}')
        return current_solution

    def solve(self):
        self.__read_input()
        ma=self.create_initial_state()
        self.solution=self.hill_climbing(ma)
        return self.solution
        
def main():
    t1=time.time()
    solver=Solver(input_file='1.txt', time_limit=10)
    hill=solver.solve()
    print(f"{hill=}")
    t2=time.time()
    print(t2-t1)

if __name__ == "__main__":
    main()