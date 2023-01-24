import logging
import time


from ortools.sat.python import cp_model


class SolutionCallback(cp_model.CpSolverSolutionCallback):
    def __init__(self, variables, time_limit = None, logger = None):
        cp_model.CpSolverSolutionCallback.__init__(self)
        self.__variables = variables
        self.solution = None
        if logger is None:
            logger = logging.getLogger()
            logging.basicConfig(level=logging.INFO)
        self.__logger = logger
        self.__time_limit = time_limit

        self.__start_time = time.time()

    def on_solution_callback(self):
        end_time = time.time()
        solve_time = end_time - self.__start_time
        self.solution = [self.Value(v) for v in self.__variables]
        print(f"A solution was found with objective value: {self.ObjectiveValue()}. Time taken: {solve_time:.2f}s")
        self.__start_time = time.time()
        if self.__time_limit is not None:
            if solve_time > self.__time_limit:
                self.StopSearch()
class Solver:

    """
    Load of each truck can be described as a weighted sum of goods' quantities where each weight can be either 0 or 1 indicating either that truck contains goods for that particular customer. Then our constraints will be:

    - For each truck: `lower_bound` <= `weight[truck_index].T @ goods_quantity` <= `upper_bound`
    
    - For each customer: `sum(weight[customer_index]) <= 1`

    - Maximize: sum(`weight.T` @ `values` for every `weight`)

    Params:
    
    - `input_file`: the path to the input data
    - `time_limit`: the amount of time allowed for the solver
    """

    def __init__(self, input_file: str = None, time_limit = None, *args):
        super().__init__(*args)
        self.__input_file = input_file
        self.__model = cp_model.CpModel()
        self.__time_limit = time_limit

    def __read_input(self):
        if self.__input_file is None:
            raise(f"No input file was specified!")
        try:
            with open(self.__input_file, "r") as inp_file:
                lines = inp_file.readlines()
                for i in lines:
                    print(i)
        except FileNotFoundError:
            raise(FileNotFoundError(f"File {self.__input_file} is invalid!"))
    
        # Process input into data
        quantity = [] # Quantity of goods ordered by customers
        value = [] # Total values of goods ordered by customers
        lower_bound = [] # The minimum load of trucks
        upper_bound = [] # The maximum load of trucks

        ## First line
        N, K = [int(val) for val in lines[0].split(" ")]

        ## The next N lines
        for line in lines[1: N + 1]:
            q, v = [int(val) for val in line.split(" ")]
            quantity.append(q)
            value.append(v)

        ## The last K lines
        for line in lines[-K:]:
            low, high = [int(val) for val in line.split(" ")]
            lower_bound.append(low)
            upper_bound.append(high)

        # Store arguments as attributes

        self.num_customers = N
        self.num_trucks = K

        self.__quantity = quantity
        self.__value = value
        self.total_value = sum(value)

        self.__lower_bound = lower_bound
        self.__upper_bound = upper_bound

    def __create_variables(self):
        self.__weights = []
        self.__variables = []
        for truck_idx in range(self.num_trucks):
            weight = [self.__model.NewBoolVar(name=f"{truck_idx} {customer_idx}") for customer_idx in range(self.num_customers)]
            self.__variables.extend(weight)
            self.__weights.append(weight)

    def __create_constraints(self):
        # For each truck, the total quantities of goods must be in range [lower_bound, upper_bound]
        for truck_idx in range(self.num_trucks):
            weight = self.__weights[truck_idx]
            self.__model.AddLinearConstraint(linear_expr=sum([weight[idx] * self.__quantity[idx] 
                                                              for idx in range(self.num_customers)]),
                                             lb=self.__lower_bound[truck_idx],
                                             ub=self.__upper_bound[truck_idx])

        # For each customer, only 1 truck contains his/her goods
        for customer_idx in range(self.num_customers):
            self.__model.Add(sum([weight[customer_idx] for weight in self.__weights]) <= 1)

        # Add the expression to be maximized: Maximize the total ordered goods' values
        self.__model.Maximize(sum([sum([weight[idx] * self.__value[idx] for idx in range(self.num_customers)]) 
                                    for weight in self.__weights]))

    def solve(self):
        
        self.__read_input()
        self.__create_variables()
        self.__create_constraints()

        solver = cp_model.CpSolver()
        if self.__time_limit:
            solver.parameters.max_time_in_seconds = self.__time_limit
        solution_callback = SolutionCallback(variables=self.__variables, time_limit=self.__time_limit)
        status = solver.Solve(model=self.__model, solution_callback=solution_callback)
        if status == cp_model.OPTIMAL or cp_model.FEASIBLE:
            self.num_deliver_packages = sum(solution_callback.solution)
            
            # Reshape the solution into a K x N one hot matrix
            solution = []
            for truck_idx in range(self.num_trucks):
                solution.append(solution_callback.solution[truck_idx * self.num_customers: (truck_idx+1) * self.num_customers])
                self.solution = solution
                self.objective_value = solver.ObjectiveValue()
        else:
            raise(Exception(f"No solution found!"))

    @property
    def plan(self):
        '''Return which goods will be delivered by which truck'''
        self.solve()
        plan = []
        for weight in self.solution:
            on_this_truck = []
            for index, elem in enumerate(weight):
                if elem == 1:
                    on_this_truck.append(index + 1)
            plan.append(on_this_truck)

        string_plan = "\n".join([f"- Truck {idx+1} contains goods of {len(plan[idx])} customers: {', '.join([str(val) for val in on_this_truck])}" for idx, on_this_truck in enumerate(plan)])
        res = f"With the maximum total values of {int(self.objective_value)}/{self.total_value}, we deliver {self.num_deliver_packages}/{self.num_customers} packages with the plan below: \n{string_plan}"
        return res

def main():
    solver = Solver(input_file="1.txt", time_limit = 3)
    print(solver.plan)


if __name__ == "__main__":
    main()