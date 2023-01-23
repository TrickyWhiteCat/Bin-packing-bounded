from setup import setup

required = ["ortools"]
setup(required)


from src.cp import cp_solver
from data_generator import generate_data

def main():
    data_path = "1.txt"
    generate_data(filename=data_path,
                  N = 20,
                  K = 5,
                  MAX_Q=10,
                  MIN_C=5,
                  MAX_C=10)
    solver = cp_solver.Solver(input_file=data_path)
    print(solver.plan)
    return

if __name__ == "__main__":
    main()