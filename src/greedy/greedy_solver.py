import csv
from ortools.linear_solver import pywraplp
from random import randint

def CreatDataModel(filename,N,K,MaxQ,MinC,MaxC):
    f = open(filename,'w')
    f.write(str(N)+' '+str(K)+'\n')

    D = [randint(1,MaxQ)*10 for i in range(N)]
    C = [randint(MinC,MaxC) for i in range(N)]

    for i in range(N):
        f.write(str(D[i])+' '+str(C[i])+'\n')
    
    x = [randint(0,K) for i in range(N)]
    # The Order i is transported by Truck x[i]

    c1 = [0 for i in range(K)]
    c2 = [0 for i in range(K)]

    for k in range(K):
        c1[k] = D[k]
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

def main():
    # CreatDataModel('Proj_17.txt',10,3,10,5,10)
    N,K,D,C,c1,c2 = Input('12.txt')
    solver = pywraplp.Solver('greedy_transfer_plan', pywraplp.Solver.GLOP_LINEAR_PROGRAMMING)
    # Create variables for the amount of goods delivered from truck j to customer i
    x = [[solver.NumVar(0, solver.infinity(), f'x[{i}][{j}]') for j in range(K)] for i in range(N)]

    # Create variables for the total amount of goods delivered by truck j
    y = [solver.NumVar(c1[j], c2[j], f'y[{j}]') for j in range(K)]

    # Sort customers by descending order of c[i]/d[i]
    customers = [(i, C[i]/D[i]) for i in range(N)]
    customers.sort(key=lambda x: -x[1])

    # For each customer i, select the truck j that maximizes c[i]/d[i] - (y[j] - c1[j])/d[i]
    for i, _ in customers:
        max_value = -1
        max_j = None
        for j in range(K):
            value = C[i]/D[i] - (y[j].solution_value() - c1[j])/D[i]
            if value > max_value:
                max_value = value
                max_j = j
        # Add constraint: x[i][j] <= D[i]
        solver.Add(x[i][max_j] <= D[i])
    
        # Add constraint: x[i][j] <= y[j]
        solver.Add(x[i][max_j] <= y[max_j])
    
        # Add constraint: y[j] <= c2[j]
        solver.Add(y[max_j] <= c2[max_j])

    # Set objective function to maximize the total value of delivered goods
    # Add objective function
    objective = solver.Objective()
    for i in range(N):
        for j in range(K):
            objective.SetCoefficient(x[i][j], C[i])
    objective.SetMaximization()

    # Solve the problem
    solver.Solve()
    # Print the solution
    solver.Solve()
    print("Solution:")
    for j in range(K):
        print(f"Truck {j} delivers {y[j].solution_value()} goods")
    '''
    # Check if the solution is optimal
    if solver.VerifySolution(1e-7, True):
        print("Solution is optimal.")
    else:
        print("Solution may not be optimal.")
'''

if __name__ == '__main__':
    main()
