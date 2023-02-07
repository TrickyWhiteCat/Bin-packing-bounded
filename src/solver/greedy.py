import logging

import numpy as np

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

    def __read_input(self):
        self.__logger.info(f"Trying to read input...")
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
            self.__logger.info(err_msg)
            raise(FileNotFoundError(err_msg))
    
        self.__logger.info(f"Processing input...")
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

        goods_pos=np.zeros(shape=(self.num_customers,self.num_trucks)) # Position of goods. Goods[customer_idx][truck_idx] ==1 means that package was put on truck with corresponding idx
        
        real_load=[0 for truck in range(self.num_trucks)]
        
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
            if goods_pos[cus_idx].sum() > 0: # Kiem tra xem hang dc dat len xe chua
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
            
        try:
            for key in prioritize:
                for order in truck_order:
                    try:
                        self.__logger.info(f"Trying to use greedy algorithm with packages sorted by {key} and trucks sorted by {order} bound")
                        goods_pos = self.__add_goods(prioritize=key, truck_order=order)
                        raise ArithmeticError("Done") # Used to break nested for loops
                    except ValueError:
                        self.__logger.error(f"Fail when using greedy algorithm with packages sorted by {key} and trucks sorted by {order} bound")
        except ArithmeticError:
            pass

        if goods_pos is None: # No solution found using all keys
            self.__logger.fatal(f"Fail to use greedy algorithm.")  
            return None

        self.__logger.info(f"Solution was get")
        self.solution = goods_pos
        self.__truck_values = (goods_pos.T @ np.array(self.__value)).astype(int)
        self.__real_load = (goods_pos.T @ np.array(self.__quantity)).astype(int)
        self.objective_value = self.__truck_values.sum()
        self.num_deliver_packages = int(goods_pos.sum())

        for truck_idx in range(self.num_trucks):
            self.__logger.debug(f"Truck {truck_idx+1}: Bounds: [{self.__lower_bound[truck_idx]}, {self.__upper_bound[truck_idx]}], Load: {self.__real_load[truck_idx]}, Goods values: {self.__truck_values[truck_idx]}")

        self.__logger.info(f"Number of goods delivered: {self.num_deliver_packages}/{self.num_customers}")
        self.__logger.info(f"Total goods' values: {self.objective_value}")

        return goods_pos.T

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
    logging.basicConfig(level=logging.INFO)
    solver = GreedySolver(input_file='data.txt')
    solution = solver.solve()

if __name__ == "__main__":
    main()