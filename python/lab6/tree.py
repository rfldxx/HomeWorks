def build_tree_recursive(h, r, f, g):
    return { r : [build_tree_recursive(h-1, F(r), f, g) for F in [f, g]] if h > 0 else [] }


def build_tree_list(h, r, f, g):
    N = 2**(h+1) - 1  # число вершин в дереве
    L = 2**h    # количество листьев в дереве
    TreeList = [0]*N
    
    TreeList[0] = r
    for i in range(0, N-L):
        TreeList[2*i+1] = f(TreeList[i])
        TreeList[2*i+2] = g(TreeList[i])
    
    return TreeList



def build_tree_iterative(h, r, f, g):
    TreeList = build_tree_list(h, r, f, g)

    N = 2**(h+1) - 1  # число вершин в дереве
    L = 2**h    # количество листьев в дереве

    shift = N - L
    TreeLayer = [ {x : []} for x in TreeList[shift:] ]

    while L > 1:
        L //= 2
        shift -= L
        newTreeLayer = [None] * L
        for i in range(L):
            newTreeLayer[i] =  { TreeList[shift + i] : [ TreeLayer[2*i], TreeLayer[2*i + 1] ] } 

        TreeLayer = newTreeLayer
        
    return TreeLayer[0]


print(build_tree_list(3, 2, lambda x : 3*x, lambda y : y+2))

TR = build_tree_recursive(3, 2, lambda x : 3*x, lambda y : y+2)
TI = build_tree_iterative(3, 2, lambda x : 3*x, lambda y : y+2)

print(build_tree_iterative(3, 2, lambda x : 3*x, lambda y : y+2))

print(TR == TI)
