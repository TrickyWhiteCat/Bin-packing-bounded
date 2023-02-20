import logging

def to_int(arr: list):
    return [[int(elem) for elem in row] for row in arr]

def to_float(arr: list):
    return [[float(elem) for elem in row] for row in arr]

def unsqueeze(arr:list):
    return [arr]

def matsum(mat):
    if not is_matrix(mat):
        raise TypeError(f"mat is not a valid matrix.")
    res = 0
    for row in mat:
        for elem in row:
            res += elem
    return res

def is_matrix(arr: list):
    '''Check if a given array is a valid matrix: consistent length of rows and columns and has exactly 2 dimensions.'''

    # Check for consistency between length of rows and columns
    n = len(arr[0])
    for row in arr:
        if len(row) != n: # Inconsistent length of rows
            return False
    # Check if the array has more than 2 dimensions
    try:
        arr[0][0][0] # Try to access the 3rd dimension
        return False
    except TypeError:
        pass
    except IndexError:
        pass
        
    return True

def zeros(shape: tuple):
    '''Return a matrix containing 0's with the given shape. Shape should be a tuple or 2 ints'''

    if len(shape) != 2:
        raise ValueError(f"shape's length should be 2 instead of {len(shape)}")

    return [[0 for col_idx in range(shape[1])] for row_idx in range(shape[0])]

def matmul(a: list, b: list, dtype = None):
    '''Multiply matrix a and matrix b where a and b are 2D arrays. a's shape should be mxn while b's shape should be nxk.'''

    # Check if a and b are valid matrices
    if not (is_matrix(a) and is_matrix(b)):
        raise TypeError(f"Inputs are not valid matrices.")

    # Check if a and b can be multiplied
    m = len(a)
    n = len(a[0])

    if len(b) != n:
        raise ValueError(f"b's 1st dimension ({len(b)}) doesn't match a's 2nd dimension ({len(a[0])}).")

    k = len(b[0])

    # Create a new matrix to store the result
    res = zeros((m, k)) # Result's shape should be m x k

    for row_idx in range(m):
        for col_idx in range(k):
            res[row_idx][col_idx] = sum([a[row_idx][i] * b[i][col_idx] for i in range(n)])

    if dtype is not None:
        res = [[dtype(elem) for elem in row] for row in res]

    return res

def transpose(mat):
    if not is_matrix(mat):
        raise TypeError("Input is not a valid matrix.")
    return [[mat[row_idx][col_idx] for row_idx in range(len(mat))] for col_idx in range(len(mat[0]))]

def transform_solution(solver):
    solution = solver.solve()
    if solution is None:
        return "No solution found!"

    goods_pos = []
    for truck_idx, truck in enumerate(solution):
        for customer_idx, goods_delivered in enumerate(truck):
            if goods_delivered:
                goods_pos.append((customer_idx + 1, truck_idx + 1))
    num_customers = len(goods_pos)
    goods_pos.sort(key = lambda x: x[0])

    return f"{num_customers}" + "\n" + "\n".join([f"{customer} {truck}" for customer, truck in goods_pos])

class GreedySolver:
    def __init__(self, input_file, logger = None, *args, **kwargs):
        self.__input_file = input_file
        if logger is None:
            logger = logging.getLogger("GreedySolver")
        self.__logger = logger
        try:
            self.__prioritize = kwargs["prioritize"]
        except KeyError:
            self.__prioritize = None

        try:
            self.__order = kwargs["order"]
        except KeyError:
            self.__order = None

        try:
            self.__from_file = kwargs["from_file"]
        except KeyError:
            self.__from_file = True

    def __read_input(self):
        self.__logger.info(f"Trying to read input...")

        if self.__from_file:
            if self.__input_file is None:
                err_msg = f"No input file was specified!"
                self.__logger.error(err_msg)
                raise(err_msg)
            try:
                self.__logger.info(f"Opening {self.__input_file}...")
                with open(self.__input_file, "r") as inp_file:
                    lines = inp_file.readlines()
            except FileNotFoundError:
                err_msg = f"File {self.__input_file} is invalid!"
                self.__logger.error(err_msg)
                raise(FileNotFoundError(err_msg))
        else:
            N, K = [int(val) for val in input().split(" ")]
            lines = [None]
            for new_line_idx in range(N+K):
                lines.append(input())

        self.__logger.info(f"Processing input...")
        # Process input into data
        quantity = [] # Quantity of goods ordered by customers
        value = [] # Total values of goods ordered by customers
        lower_bound = [] # The minimum load of trucks
        upper_bound = [] # The maximum load of trucks

        ## First line
        if self.__from_file:
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

        self.objective_value = 0
        self.num_deliver_packages = 0

        self.__logger.info("Input was processed")

    def __add_goods(self, prioritize: str = "quantity", truck_order: str = "lower"):
        if prioritize == "quantity":
            customer_rate=[(i, self.__quantity[i]) for i in range(self.num_customers)]
        if prioritize == "value":
            customer_rate=[(i, self.__value[i]) for i in range(self.num_customers)]
        if prioritize == "efficiency":
            customer_rate=[(i, self.__value[i]/self.__quantity[i]) for i in range(self.num_customers)]
        if prioritize == "importance":
            # Scaling down values and quantity to a range of [min_importance, 1]
            max_val = max(self.__value)
            min_val = min(self.__value)
            if min_val == max_val:
                min_val = 0
            max_quantity = max(self.__quantity)
            min_quantity = min(self.__quantity)
            if min_quantity == max_quantity:
                min_quantity = 0
            values = []
            quantities = []

            min_importance = 0.1 # This is the minimum importance. It's defined because the importance of a package should not be 0
            for idx in range(self.num_customers):
                values.append((self.__value[idx] - min_val) / (max_val - min_val) * (1 - min_importance) + min_importance)
                quantities.append((self.__quantity[idx] - min_quantity) / (max_quantity - min_quantity) * (1 - min_importance) + min_importance)

            # Adding importance as the key to the sorting function
            customer_rate = []
            order = 0.5
            for idx in range(self.num_customers):
                importance = values[idx] * (quantities[idx] ** order) # Since each quantity here should be smaller than 1, its power should be smaller than itself.
                customer_rate.append((idx, importance))

        self.__logger.info("Sorting customers...")
        customer_rate.sort(key=lambda x: -x[1]) # Sort giam dan theo value
        self.__logger.info("Done")


        self.__logger.info(f"Sorting trucks by {truck_order} bounds...")
        if truck_order == "lower":
            truck_rate=[(i, -self.__lower_bound[i]) for i in range(self.num_trucks)] # Sort in descending order
        if truck_order == "upper":
            truck_rate=[(i, -self.__upper_bound[i]) for i in range(self.num_trucks)] # Sort in descending order
        if truck_order == "difference":
            truck_rate=[(i, self.__upper_bound[i] - self.__lower_bound[i]) for i in range(self.num_trucks)] # Sort in ascending order
        truck_rate.sort(key=lambda x: x[1])
        self.__logger.info("Done")

        goods_pos = zeros(shape=(self.num_customers,self.num_trucks)) # Position of goods. Goods[customer_idx][truck_idx] ==1 means that package was put on truck with corresponding idx

        real_load = [0 for truck in range(self.num_trucks)]

        self.__logger.info("Adding goods to match trucks lower bound...")
        for cus_idx, rate in customer_rate:

            q_customer= self.__quantity[cus_idx]

            # Nhet du lower
            for truck_idx, rate in truck_rate: # Chon xe
                lower = self.__lower_bound[truck_idx]
                upper = self.__upper_bound[truck_idx]

                if real_load[truck_idx] < lower and real_load[truck_idx] + q_customer <= upper: # nhet du lower da
                    real_load[truck_idx] += q_customer
                    goods_pos[cus_idx][truck_idx]=1
                    break
        self.__logger.info(f"Done")

        # Check lai xem du lower bound chua
        self.__logger.info(f"Checking lower bound condition...")
        for truck_idx, rate in truck_rate:
            if real_load[truck_idx] < self.__lower_bound[truck_idx]:
                err_msg = f"Truck {truck_idx} with lower bound {self.__lower_bound[truck_idx]} only contains {real_load[truck_idx]} packages"
                self.__logger.error(err_msg)
                raise ValueError(err_msg)
        self.__logger.info(f"Condition satisfied.")


        # Toi day la co du lower bound r, phai check xem hang dc nhet vao xe chua, chua dc nhet thi minh nhet vao
        self.__logger.info("Adding goods until full...")
        for cus_idx, rate in customer_rate:
            if sum(goods_pos[cus_idx]) > 0: # Kiem tra xem hang dc dat len xe chua
                continue 

            q_customer = self.__quantity[cus_idx]

            # Nhet du lower
            for truck_idx, rate in truck_rate: # Chon xe
                lower = self.__lower_bound[truck_idx]
                upper = self.__upper_bound[truck_idx]

                if real_load[truck_idx] + q_customer <= upper: # nhet vua xe
                    real_load[truck_idx] += q_customer
                    goods_pos[cus_idx][truck_idx]=1
                    break
                    
        self.__logger.info(f"Done")

        return goods_pos


    def solve(self):
        self.__read_input()

        goods_pos = None
        if self.__prioritize is None:
            prioritize = ["efficiency", "value", "importance", "quantity"]
        else:
            prioritize = [self.__prioritize]

        if self.__order is None:
            truck_order = ["lower", "upper", "difference"]
        else:
            truck_order = [self.__order]

        for key in prioritize:
            for order in truck_order:
                try:
                    self.__logger.info(f"Trying to use greedy algorithm with packages sorted by {key} and trucks sorted by {order} bound")
                    goods_pos = self.__add_goods(prioritize=key, truck_order=order)
                    break
                except ValueError:
                    self.__logger.error(f"Fail when using greedy algorithm with packages sorted by {key} and trucks sorted by {order} bound")

        if goods_pos is None: # No solution found using all keys
            self.__logger.fatal(f"Fail to use greedy algorithm.")  
            return None

        self.__logger.info(f"Solution was get")
        self.solution = goods_pos
        self.__truck_values = matmul(transpose(goods_pos), transpose(unsqueeze(self.__value)), dtype=int)
        self.__real_load = matmul(transpose(goods_pos), transpose(unsqueeze(self.__quantity)), dtype=int)
        self.objective_value = matsum(self.__truck_values)
        self.num_deliver_packages = int(matsum(goods_pos))

        for truck_idx in range(self.num_trucks):
            self.__logger.debug(f"Truck {truck_idx+1}: Bounds: [{self.__lower_bound[truck_idx]}, {self.__upper_bound[truck_idx]}], Load: {self.__real_load[truck_idx]}, Goods values: {self.__truck_values[truck_idx]}")

        self.__logger.info(f"Number of goods delivered: {self.num_deliver_packages}/{self.num_customers}")
        self.__logger.info(f"Total goods' values: {self.objective_value}")

        return transpose(goods_pos)

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
    logging.basicConfig(level=logging.FATAL+1)
    solver = GreedySolver(input_file='data.txt', from_file = False)
    print(transform_solution(solver))

if __name__ == "__main__":
    main()