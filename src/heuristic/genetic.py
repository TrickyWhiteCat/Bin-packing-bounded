import random
import sys
import operator

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

    def __read_input(self)->None:
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

    def check_constraints(self, matrix:np) ->bool:
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
    
    def create_initial_state(self)->np:
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
    def create_neighbour(self,matrix:np)->np: #dynamic neighbourhood size
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

    def objective_function(self,matrix:np)->int:
        self.__read_input()
        num_customers=self.num_customers
        num_trucks=self.num_trucks
        quantity=self.__quantity
        value=self.__value 
        lower_bound=self.__lower_bound
        upper_bound=self.__upper_bound
        
        K=np.ones(num_trucks,)
        return (value@matrix)@K

    def generate_initial_population(self,size:int)->list:
        population = set()
        matrix=self.create_initial_state()
        if self.check_constraints(matrix):
            a=[tuple(i) for i in matrix]
            population.add(tuple(a))
        # generate initial population having `count` individuals
        while len(population) != size:
            # pick random bits one for each item and 
            # create an individual 
            a=[tuple(i) for i in self.create_neighbour(matrix)]
            population.add(tuple(a))

        return [np.array(individual) for individual in population]
    
    def fitness(self,matrix:np)->int:
        if self.check_constraints(matrix):
            return self.objective_function(matrix)
        return 0
    
    def selection(self,population:list)->list:
        parents = []
        # randomly shuffle the population
        shuffle(population)
        # while len(parents) < 2:
        # we use the first 4 individuals
        # run a tournament between them and
        # get two fit parents for the next steps of evolution

        # tournament between first and second
        if self.fitness(population[0]) > self.fitness(population[1]) :
            parents.append(population[0])
        elif  self.fitness(population[0]) < self.fitness(population[1]):
            parents.append(population[1])

        # tournament between third and fourth
        if self.fitness(population[2]) > self.fitness(population[3]):
            parents.append(population[2])
        # elif self.fitness(population[2]) < self.fitness(population[3]):
        else:
            parents.append(population[3])
            # shuffle(population)

        return parents
    
    def crossover(self,parents: list) -> list:
        N = self.num_customers
        threshold=N//2
        child1 = np.concatenate((parents[0][:threshold],parents[1][threshold:]))
        child2 = np.concatenate((parents[0][threshold:],parents[1][:threshold]))

        return [child1,child2]
    
    def mutate(self,individuals:np,MUTATION_RATE) -> np:
        for individual in individuals:
            for i,customer in enumerate(individual):
                if random() > MUTATION_RATE:
                    temp=list(customer)
                    lst=self.create_binary()
                    lst.remove(temp)
                    individual[i]=choice(lst)
        return individuals
    
    def next_generation(self,population:list,REPRODUCTION_RATE,CROSSOVER_RATE,MUTATION_RATE) -> list:
        next_gen = []
        while len(next_gen) < len(population):
            children = []

            # we run selection and get parents
            parents = self.selection(population)

        # reproduction
            if random() < REPRODUCTION_RATE:
                children = parents
            else:
                # crossover
                if random() < CROSSOVER_RATE:
                    children = self.crossover(parents)

            # mutation
                if random() < MUTATION_RATE:
                    self.mutate(children,MUTATION_RATE)

            next_gen.extend(children)

        return next_gen
    
    def Genetic(self,size:int,num_generation:int,REPRODUCTION_RATE:float,CROSSOVER_RATE:float,MUTATION_RATE:float) ->int:
        population=self.generate_initial_population(size)
        self.__read_input()
        num_customers=self.num_customers
        num_trucks=self.num_trucks
        quantity=self.__quantity
        value=self.__value 
        lower_bound=self.__lower_bound
        upper_bound=self.__upper_bound
        # while True:
        for t in range(num_generation):
            
            population=self.next_generation(population,REPRODUCTION_RATE,CROSSOVER_RATE,MUTATION_RATE)
            
        population = sorted(population, key=lambda i: self.fitness(i), reverse=True)
        solution=population[0]
        K=np.ones(num_trucks,)
            # if  (value@solution)@K >= 131:
            #     break

        
        return self.check_constraints(solution), solution.sum(),(value@solution)@K
    
t1=time.time()
solver=Solver(input_file='1.txt')
final=solver.Genetic(50,500,0.3,0.4,0.01)
print(final)
t2=time.time()
print(t2-t1)
    
	