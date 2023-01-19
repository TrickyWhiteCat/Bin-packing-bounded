from ortools.sat.python import cp_model


class SolutionCallback(cp_model.CpSolverSolutionCallback):
    def __init__(self, variables):
        cp_model.CpSolverSolutionCallback.__init__(self)
        self.__variables = variables
        self.solution = None

    def on_solution_callback(self):
        self.solution = [self.Value(v) for v in self.__variables]

class Solver:

    """
    Load of each truck can be described as a weighted sum of goods' quantities where each weight can be either 0 or 1 indicating either that truck contains goods for that particular customer. Then our constraints will be:

    - For each truck: `lower_bound` <= `weight[truck_index].T @ goods_quantity` <= `upper_bound`
    
    - For each customer: `sum(weight[customer_index]) <= 1`

    - Maximize: sum(`weight` @ `values` for every `weight`)
    """

    def __init__(self, input_file = None, *args):
        super().__init__(*args)
        self.__input_file = input_file
        self.__model = cp_model.CpModel()

    def __read_input(self):
        if self.__input_file is None:
            raise(f"No input file was specified!")
        try:
            with open(self.__input_file, "r") as inp_file:
                lines = inp_file.readlines()
        except FileNotFoundError:
            raise(f"File {self.__input_file} is invalid!")
    
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
        solution_callback = SolutionCallback(variables=self.__variables)
        status = solver.Solve(model=self.__model, solution_callback=solution_callback)
        if status == cp_model.OPTIMAL:
            self.num_deliver_packages = sum(solution_callback.solution)
            # Reshape solution into a K x N one hot matrix
            solution = []
            for truck_idx in range(self.num_trucks):
                solution.append(solution_callback.solution[truck_idx * self.num_customers: (truck_idx+1) * self.num_customers])
                self.solution = solution
                self.objective_value = solver.ObjectiveValue()
        else:
            raise(f"No optimal solution found!")

    @property
    def plan(self):
        '''Return which goods will be delivered by which truck'''
        plan = []
        for weight in self.solution:
            on_this_truck = []
            for index, elem in enumerate(weight):
                if elem == 1:
                    on_this_truck.append(index + 1)
            plan.append(on_this_truck)

        string_plan = "\n".join([f"- Truck {idx+1} contains goods of customers {', '.join([str(val) for val in plan[idx]])}" for idx in range(len(plan))])
        return string_plan

if __name__ == "__main__":
    solver = Solver(input_file="1.txt")
    solver.solve()
    print(f"With the maximum total values of {int(solver.objective_value)}/{solver.total_value}, we deliver {solver.num_deliver_packages}/{solver.num_customers} packages with the plan below: \n{solver.plan}")