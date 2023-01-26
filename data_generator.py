import random as rd

def generate_data(filename,N,K,MAX_Q,MIN_C, MAX_C):
    '''Generate data with format:
    First line: `N` `K`

    Each of the next `N` lines contains the quantity of goods ordered by each customer and the respective total values

    Each of the last `K` lines contains the lower and upper bound of each truck.

    E.g.:\n
    10 2\n
    70 9\n
    100 7\n
    50 8\n
    80 8\n
    50 10\n
    100 7\n
    100 9\n
    50 6\n
    80 7\n
    40 10\n
    200 234\n
    240 240\n
    '''
    with open(filename, "w") as f:
        f.write(f"{N} {K}\n")

    w = [rd.randint(1,MAX_Q)*10 for i in range(N)] # quantity/weight of goods
    c = [rd.randint(MIN_C,MAX_C) for i in range(N)] # total cost of these goods were generated by MIN_C and MAX_C
    
    # Generate random SOLUTION 
    x = [rd.randint(0,K) for i in range(N)] # x[i] is the index of the truck carrying the order i randomly (to ensure having feasible solution)
    load = [0 for k in range(K)]
    c1 = [0 for k in range(K)] # minimum weight of each truck
    c2 = [0 for k in range(K)] # maximum weight of each truck 
    
    for k in range(K):
        for i in range(N):
            if x[i]==k:
                load[k]=load[k]+w[i]
        c1[k]=load[k] # total random weight is lower bound

        max_load_range = 40
        c2[k]=c1[k] + rd.randint(0,max_load_range) # random upper bound
    
    with open(filename, "a") as f:
        for i in range(N):
            f.write(f"{w[i]} {c[i]}\n")
        for k in range(K):
            f.write(f"{c1[k]} {c2[k]}\n")

if __name__ == "__main__":
    generate_data(filename='data.txt',
                  N=40,
                  K=5,
                  MAX_Q=10,
                  MIN_C=5,
                  MAX_C=10)







