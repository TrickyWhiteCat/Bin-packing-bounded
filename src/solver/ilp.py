import logging


from ortools.linear_solver import pywraplp

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

    return N,K,D,C,c1,c2

class ILPSolver:
    def __init__(self, input_file: str = None, logger = None, *args):
        self.__input_file = input_file
        if logger is None:
            logger = logging.getLogger("CPSolver")
        self.__logger = logger

    def solve(self):
        N,K,D,C,c1,c2 = Input(self.__input_file)
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
    
        if status == pywraplp.Solver.OPTIMAL or pywraplp.Solver.FEASIBLE:
        
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
                print('\n- Truck {} contains goods of {} customers: {}'.format(j+1,len(on_this_truck[j]),', '.join([str(x+1) for x in on_this_truck[j]])))
        else:
            print('No Solution!')

    def plan(self):
        "Alias for consistency between solvers"
        self.solve()

def main():
    solver = ILPSolver(input_file="1.txt")
    solver.solve()

if __name__ == '__main__':
    main()

