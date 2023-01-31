from setup import setup
required = ["ortools", "numpy"]
setup(required)


import logging
import time

from src import GreedySolver, CPSolver, ILPSolver, HillClimbing, SimulatedAnnealing
from src.solver.utils.data_generator import generate_data

def main():

    data_path = "data.txt"

    generate_data(filename=data_path,
                  N = 50,
                  K = 5,
                  MAX_Q=10,
                  MIN_C=5,
                  MAX_C=10)
    time_limit = 3

    # Initialize solvers
    solvers= [GreedySolver(input_file=data_path),
              HillClimbing(input_file=data_path),
              SimulatedAnnealing(input_file=data_path),
              CPSolver(input_file=data_path, use_greedy=False, time_limit=time_limit, log_cp_sat_process = False),
              ILPSolver(input_file=data_path, time_limit=time_limit),
              CPSolver(input_file=data_path, use_greedy=True, time_limit=time_limit, log_cp_sat_process = False)]


    # Test all solver
    for solver in solvers:
        print(type(solver))
        start = time.time()
        res = solver.plan()
        print(res)
        print(f"Execution time: {time.time() - start:.2f}s\n")

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, filename="main.log", filemode="w") # Head to this file to see the full log.
    main()