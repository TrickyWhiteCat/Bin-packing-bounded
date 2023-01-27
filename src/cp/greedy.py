import logging

import numpy as np

class GreedySolver:
    def __init__(self, input_file, logger = None, *args):
        self.__input_file = input_file
        if logger is None:
            logger = logging.getLogger("GreedySolver")
        self.__logger = logger

    def __read_input(self):
        self.__logger.info(f"Trying to read input...")
        if self.__input_file is None:
            self.__logger.error(f"No input file was specified!")
            raise(f"No input file was specified!")
        try:
            self.__logger.info(f"Opening {self.__input_file}...")
            with open(self.__input_file, "r") as inp_file:
                lines = inp_file.readlines()
        except FileNotFoundError:
            self.__logger.info(f"File {self.__input_file} is invalid!")
            raise(FileNotFoundError(f"File {self.__input_file} is invalid!"))
    
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

        self.__logger.info("Input was processed")


    def solve(self):
        self.__read_input()
        
        self.__logger.info("Sorting customers...")
        customer_rate=[(i, self.__value[i]) for i in range(self.num_customers)]
        customer_rate.sort(key=lambda x: -x[1]) # Sort giam dan theo value
        self.__logger.info("Done")

        self.__logger.info("Sorting customers...")
        truck_rate=[(i, self.__lower_bound[i]) for i in range(self.num_trucks)]
        truck_rate.sort(key=lambda x: -x[1])
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
                self.__logger.error(f"Truck {truck_idx} with lower bound {self.__lower_bound[truck_idx]} only contains {real_load[truck_idx]} packages")
                raise ValueError(f"Truck {truck_idx} with lower bound {self.__lower_bound[truck_idx]} only contains {real_load[truck_idx]} packages")
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
        self.__logger.info(f"Solution was get")
        self.__truck_values = (goods_pos.T @ np.array(self.__value)).astype(int)
        self.objective_value = self.__truck_values.sum()
        self.num_deliver_packages = int(goods_pos.sum())

        for truck_idx in range(self.num_trucks):
            self.__logger.info(f"Truck {truck_idx+1}: Bounds: [{self.__lower_bound[truck_idx]}, {self.__upper_bound[truck_idx]}], Load: {real_load[truck_idx]}, Goods values: {self.__truck_values[truck_idx]}")

        self.__logger.info(f"Number of goods delivered: {int(goods_pos.sum())}/{self.num_customers}")
        self.__logger.info(f"Total goods' values: {self.objective_value}")

        return goods_pos
    
def main():
    logging.basicConfig(level=logging.INFO)
    solver=GreedySolver(input_file='1.txt')
    mat=solver.solve()

if __name__ == "__main__":
    main()
   
                    
                    
                    
        







