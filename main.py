from setup import setup
required = ["ortools", "numpy"]
setup(required)


import logging
import time

from src import GreedySolver, CPSolver, ILPSolver
from data_generator import generate_data

def main():

    data_path = "data.txt"

    generate_data(filename=data_path,
                  N = 50,
                  K = 5,
                  MAX_Q=10,
                  MIN_C=5,
                  MAX_C=10)

    # Initialize solvers
    greedy_solver = GreedySolver(input_file=data_path)
    cp_solver = CPSolver(input_file=data_path, use_greedy=True, time_limit=10, log_cp_sat_process = False)
    ilp_solver = ILPSolver(input_file=data_path, time_limit=10)

    # Test all solver
    for solver in [greedy_solver, cp_solver, ilp_solver]:
        print(type(solver))
        start = time.time()
        res = solver.plan()
        print(res)
        print(f"Execution time: {time.time() - start:.2f}s\n")

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, filename="main.log", filemode="w") # Head to this file to see the full log.
    main()