from setup import setup
required = ["ortools", "numpy"]
setup(required)


import logging
import time

from src import GreedySolver, CPSolver, ILPSolver, HillClimbing, SimulatedAnnealing
from src.solver.utils.data_generator import generate_data
from src.solver.utils.solution_transformer import transform_solution

def main():

    data_path = "data.txt"

    '''generate_data(filename=data_path,
                  N = 50,
                  K = 5,
                  MAX_Q=10,
                  MIN_C=5,
                  MAX_C=10)'''
    time_limit = None

    # Initialize solvers
    solvers= [GreedySolver(input_file=data_path),
              #CPSolver(input_file=data_path, use_greedy=False, time_limit=time_limit, log_cp_sat_process = True),
              #ILPSolver(input_file=data_path, time_limit=time_limit),
              CPSolver(input_file=data_path, use_greedy=True, time_limit=time_limit, log_cp_sat_process = True)]


    # Test all solver
    for solver in solvers:
        print(type(solver))
        res = transform_solution(solver)
        if res != "No solution found!":
            print("Found solution")
            with open("result.txt", "w") as res_file:
                res_file.write(res)
            break


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, filemode="w") # Head to this file to see the full log.
    main()