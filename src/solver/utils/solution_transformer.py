def transform_solution(solver):
    import numpy as np
    solution = solver.solve()
    if solution is None:
        return "No solution found!"
    solution = np.array(solution)
    delivered = solution.T.sum(axis=1) != 0 # Sum == 0 means that that package haven't been delivered
    trucks = (solution.T.argmax(axis=1) + 1) * delivered
    customers = range(1, solver.num_customers + 1)
    num_customers = np.sum(delivered)
    return f"{num_customers}" + "\n" + "\n".join([f"{customer} {truck}" for customer, truck in zip(customers, trucks) if truck != 0])