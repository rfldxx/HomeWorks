import matplotlib.pyplot as plt
import numpy as np
from itertools import repeat

def test_func(f, n):
    if( f(n) != factorial(n) ): raise ValueError(f"Value of f({n}) != {n}!")

def benchmark(f, n, num_repeats=10, num_runs=10):
    Times = timeit.repeat(lambda: f(n), repeat=num_repeats, number=num_runs)
    return sum(Times) / (num_repeats*num_runs)

def graph(nn, funcs, names=[]):
    if( names == [] ):
        names = [ f"func[{i}]" for i in range(len(funcs)) ]
    
    times = [[] for _ in range(len(funcs))]

    for i, f in enumerate(funcs):
        for n in nn:
            try:
               test_func(f, n)
            except ValueError:
                print(f"Error in function {names[i]} on value n = {n}!")
            
            times[i].append( benchmark(f, n) )
        
        print("Final with", names[i], " last n =", nn[-1], " needed time = ", times[i][-1])


    # Построение графика
    plt.figure(figsize =(10, 7))
    plt.xticks(nn)
    for i, f_times in enumerate(times):
        plt.plot(nn, f_times, marker='o', label=names[i], linewidth=2)
    
    plt.xlabel('n')
    plt.ylabel('t, секунды')
    plt.legend()
    plt.show()
    
    
    
    

def T_Small():
    nn = [50, 100, 250, 500, 750, 1000]
    names = ['factorial', 'fact_recursive', 'fact_classic', 'fact_classic_1', 'fact3', 'fact3_1', 'fact5', 'fact6', 'fact6_1']
    funcs = [ factorial ,  fact_recursive ,  fact_classic ,  fact_classic_1 ,  fact3 ,  fact3_1 ,  fact5 ,  fact6 ,  fact6_1 ]

    graph(nn, funcs, names)
  
def T_Large():
    nn = [1000, 2000, 3000, 4000, 5000, 7500, 10000, 12500, 15000, 17500, 20000, 22500, 25000]
    names = ['factorial', 'fact_recursive', 'fact_classic', 'fact_classic_1', 'fact3', 'fact3_1', 'fact5', 'fact6', 'fact6_1']
    funcs = [ factorial ,  fact_recursive ,  fact_classic ,  fact_classic_1 ,  fact3 ,  fact3_1 ,  fact5 ,  fact6 ,  fact6_1 ]

    graph(nn, funcs, names)


    

# benchmark(fact_classic, 5000, 100, 4)
T_Large()
