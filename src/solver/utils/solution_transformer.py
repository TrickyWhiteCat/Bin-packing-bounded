def transform_solution(solver):
    import numpy as np
    solution = solver.solve()
    if solution is None:
        return "No solution found!"
    trucks = np.array(solution).T.argmax(axis=1) + 1
    customers = range(1, solver.num_customers + 1)
    num_customers = len(trucks)
    return f"{num_customers}" + "\n" + "\n".join([f"{customer} {truck}" for customer, truck in zip(customers, trucks)])