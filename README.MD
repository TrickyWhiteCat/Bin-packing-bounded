# BIN PACKING LOWER, UPPER BOUND

## Problem description

There exist N customers 1, 2,..., N where customer `i` ordered `d[i]` quantity of goods with the total value of `c[i]`. There are K trucks 1, 2,..., K transfering goods where truck `k` has a minimum load of `c1[k]` and maximum load of `c2[k]`. Compute the tranfering plan sastifying:

- Each customer takes goods from only 1 truck.
- The total amount of goods on each truck must be in the range of the minimum and maximum loads of it.
- The total values of delivered goods must be maximized.

## Algorithm
- [x] Greedy
- [x] Integer Linear Programming (ILP)
- [x] Constraint Programming (CP)
- [x] Heuristic - constraint based local search

## How to run
####1. Run all models on a new dataset
- Run the `main.py` script:
```console
$python <path_to_repo>/main.py
```
or
```console
$python3 <path_to_repo>/main.py
```
On this `main.py` script, we generate a new dataset stored in `data.txt` file, initialize all models and run them on that dataset.
####2. Run one or more models on a given dataset
   
- Models can be simply imported to a new python script or jupyter notebook:
```python
from src import GreedySolver, CPSolver, ILPSolver, HillClimbing, SimulatedAnnealing
```
- Initialize the model with a path to the input file and some other arguments:
```python
model = GreedySolver(input_file=data_path)
```
_For more information about solvers' specific arguments, head to the implementation of it._
_Note that most solvers needs other components and external libraries to work properly except for `IndependentGreedySolver` inside `greedy_no_numpy.py`. It's also the only solver currently supporting inputting from the console instead of a text file._

- Solve the problem:
```python
model.plan()
```
This line of code will print to the default print stream a plan for delivery. To gather the raw result which is a decision matrix, use
```python
model.solve()
```
####3. Get the model's attribute
In the solving process, it's helpful to get some of the solution's statistic:
- `model.objective_value`: return the current objective value of the model
- `model.num_deliver_packages`: return the number of packages which can be delivered.
- `model.total_value`: the total value of goods. Also an upper bound for `model.objective_value`.
- `model.num_customers`: the number of customers