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

def main():
    # CreatDataModel('Proj_17.txt',10,3,10,5,10)
    N,K,D,C,c1,c2 = Input('12.txt')
    solver = pywraplp.Solver.CreateSolver('SCIP')
    if not solver:
        return
    
    # SetVariables:

    # x[i][j] = 1 if item i is packed by truck j
    x = [[0 for col in range(K)] for row in range(N)]
    for row in range(N):
        for col in range(K):
            x[row][col] = solver.IntVar(0,1,'x[{}][{}]'.format(row,col))

    # Constraints
    # Each item must be packed by exactly 1 truck
    for row in range(N):
        solver.Add(sum(x[row]) <= 1)

    # The amount packed in each bin is greater than LB and less than UB
    for j in range(K):
        solver.Add(sum([x[i][j]*D[i] for i in range(N)]) >= c1[j])
        solver.Add(sum([x[i][j]*D[i] for i in range(N)]) <= c2[j])
    
    obj = []
    for j in range(K):
        for i in range(N):
            obj.append(x[i][j] * C[i])
    solver.Maximize(sum(obj))

    status = solver.Solve()

    if status == pywraplp.Solver.OPTIMAL:

        on_this_truck = [[] for j in range(K)]
        order_delivered = 0

        for i in range(N):
            for j in range(K):
                if int(x[i][j].solution_value()) == 1:
                    on_this_truck[j].append(i)
                    order_delivered += 1

        print('Integer Linear Program Solution:')
        print('With the maximum total values of {}/{}, we deliver {}/{} packages with the plan below:'.format(int(solver.Objective().Value()),sum(C),order_delivered,N))
        for j in range(K):
            print('- Truck {} contains goods of {} customers: {}'.format(j+1,len(on_this_truck[j]),', '.join([str(x+1) for x in on_this_truck[j]])))
    else:
        print('No Solution!')

if __name__ == '__main__':
    main()

