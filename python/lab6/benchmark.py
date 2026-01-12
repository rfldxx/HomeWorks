import matplotlib.pyplot as plt
import numpy as np
from itertools import repeat
import timeit

def test_func(F, G, args):
    if( F(*args) != G(*args) ): raise ValueError()

def benchmark(F, args, num_repeats=10, num_runs=10):
    Times = timeit.repeat(lambda: F(*args), repeat=num_repeats, number=num_runs)
    return sum(Times) / (num_repeats*num_runs)

def graph(nargs, funcs, names=[]):
    if( names == [] ):
        names = [ f"func[{i}]" for i in range(len(funcs)) ]
    
    times = [[] for _ in range(len(funcs))]

    for i, f in enumerate(funcs):
        for args in nargs:            
            times[i].append( benchmark(f, args) )
  

    # Построение графика
    plt.figure(figsize =(10, 7))

    hh = [args[0] for args in nargs]
    plt.xticks(hh)
    for i, f_times in enumerate(times):
        plt.plot(hh, f_times, marker='o', label=names[i], linewidth=2)
    
    plt.xlabel('n')
    plt.ylabel('t, секунды')
    plt.legend()
    plt.show()
    
    
    
    

def T_Small():
    nargs = [ [h, 1, lambda x : x+1, lambda x : x+1] for h in range(0, 15+1) ]
    names = ['build_tree_iterative', 'build_tree_recursive', 'build_tree_list']
    funcs = [ build_tree_iterative ,  build_tree_recursive ,  build_tree_list ]

    for args in nargs:
        test_func(build_tree_iterative, build_tree_recursive, args)

    graph(nargs, funcs, names)
  
    
T_Small()
