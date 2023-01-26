from setup import setup
required = ["ortools", "numpy"]
setup(required)


import logging


from src.solver import cp
from data_generator import generate_data

def main():
    data_path = "12.txt"
    generate_data(filename=data_path,
                  N = 2000,
                  K = 5,
                  MAX_Q=10,
                  MIN_C=5,
                  MAX_C=10)
    solver = cp.CPSolver(input_file=data_path, time_limit=10, use_greedy=True)
    print(solver.plan)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    main()