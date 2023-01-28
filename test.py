from setup import setup
required = ["ortools", "numpy"]
setup(required)


import logging
import time

from src import GreedySolver, CPSolver, ILPSolver
from data_generator import generate_data

def test(N, K, time_limit:int = 60, data_path:str = None, result_file:str = None, create_new_data:bool = True):
    if data_path is None:
        data_path = f"data_{N}_{K}.txt"
    if result_file is None:
        result_file = f"result_{N}_{K}.csv"
    
    if create_new_data:
        generate_data(filename=data_path,
                      N=N,
                      K=K,
                      MAX_Q=10,
                      MIN_C=5,
                      MAX_C=10)

    # Initialize solvers
    solvers = [GreedySolver(input_file=data_path),
               CPSolver(input_file=data_path, use_greedy=False, time_limit=time_limit, log_cp_sat_process = False),
               ILPSolver(input_file=data_path, time_limit=time_limit),
               CPSolver(input_file=data_path, use_greedy=True, time_limit=time_limit, log_cp_sat_process = False),]

    # Test all solver
    obj_val = []
    delivered = []
    execution_time = []

    for idx, solver in enumerate(solvers):
        start = time.time()
        solver.solve()
        end = time.time()
        execution_time.append(end-start)
        obj_val.append(solver.objective_value/solver.total_value)
        delivered.append(solver.num_deliver_packages/solver.num_customers)
        
    solver_names = ["greedy", "cp", "ilp", "cp_greedy"]
    with open(result_file, "a") as res_file:
        to_write = []
        for idx, name in enumerate(solver_names):
            to_write.extend([obj_val[idx],delivered[idx],execution_time[idx]])
        res_file.write(f"{','.join([str(elem) for elem in to_write])}\n")

def create_heading(prefix:str = None): # Helper function
    if prefix is None:
        prefix = ""
    if prefix[-1] != "_": # Add "_" to seperate prefix from other components
        prefix += "_"
    return f"{prefix}value_rate,{prefix}deliver_rate,{prefix}exec_time"

def main():
    num_trials = 100
    N = 10
    K = 50
    time_limit = 60

    data_path = f"data_{N}_{K}.txt"
    result_file = f"result_{N}_{K}.csv"

    with open(result_file, "w") as res_file:
        # Write headline
        solver_names = ["greedy", "cp", "ilp", "cp_greedy"]
        for key in solver_names:
            res_file.write(create_heading(key))
        res_file.write("\n")

    for trial in range(num_trials):
        print(f"Trial {trial}/{num_trials}", end="\r")
        
        test(N=N, K=K, time_limit=time_limit, data_path=data_path, result_file=result_file)

    print(f"Testing {num_trials} times with {N = }, {K = } was done.")

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, filename="test.log", filemode="w") # Head to this file to see the full log.
    main()