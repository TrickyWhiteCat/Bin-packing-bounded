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
    def __init__(self, input_file: str = None, time_limit:int = None, logger = None, *args):
        self.__input_file = input_file
        if logger is None:
            logger = logging.getLogger("ILPSolver")
        self.__logger = logger
        self.solution = None
        self.objective_value = 0
        self.num_deliver_packages = 0
        self.__time_limit = time_limit

    def solve(self):
        self.__logger.info("Solving...")
        self.__logger.info("Reading input...")
        N,K,D,C,c1,c2 = Input(self.__input_file)
        self.num_customers = N
        self.num_trucks = K
        self.total_value = sum(C)
        self.__logger.info("Done")
        self.__logger.info("Ortools' solver was created")
        solver = pywraplp.Solver.CreateSolver('SCIP')
        if self.__time_limit is not None:
            solver.SetTimeLimit(1000*self.__time_limit)
            self.__logger.info(f"Time limit was set to {self.__time_limit}")
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

        self.__logger.info("Solving using Ortools' SCIP...")
        status = solver.Solve()
    
        if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
            self.__logger.info("Solution was get")
            self.objective_value = solver.Objective().Value()
        
            order_delivered = 0

            solution = []
            for i in range(N):
                line = []
                for j in range(K):
                    x_i_j = int(x[i][j].solution_value())
                    line.append(x_i_j)
                    if x_i_j == 1:
                        order_delivered += 1
                solution.append(line)

            self.num_deliver_packages = order_delivered
            import numpy as np
            self.solution = np.array(solution).T
            
        return self.solution

    def plan(self):
        self.solution = self.solve()
        if self.solution is None:
            return f"No solution found"
        plan = []
        for weight in self.solution:
            on_this_truck = []
            for index, elem in enumerate(weight):
                if elem == 1:
                    on_this_truck.append(index + 1)
            plan.append(on_this_truck)

        string_plan = "\n\n".join([f"- Truck {idx+1} contains goods of {len(plan[idx])} customers: {', '.join([str(val) for val in on_this_truck])}" for idx, on_this_truck in enumerate(plan)])
        res = f"With the maximum total values of {int(self.objective_value)}/{self.total_value}, we deliver {self.num_deliver_packages}/{self.num_customers} packages with the plan below: \n{string_plan}"
        return res

def main():
    solver = ILPSolver(input_file="1.txt", time_limit=10)
    print(solver.plan())

if __name__ == '__main__':
    main()

