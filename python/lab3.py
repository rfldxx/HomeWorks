### В ПРОЦЕССЕ . . .


from typing import Tuple, List, Callable, Dict, Any

def gen_bin_tree(h : int, r : int, f : Callable[[int], int], g : Callable[[int], int]) -> Dict[int, Tuple[Any, Any]]:
    return { str(r) : [gen_bin_tree(h-1, F(r), f, g) for F in [f, g]] if h else [] }

gen_bin_tree(3, 1, lambda x: x+1, lambda y: y*3)

# gen_bin_tree(3, 1, lambda x: x+1, lambda y: y*3) :
# redurned:
#  {'1': 
#      [{'2':
#          [{'3':
#              [{'4': []},
#              {'9': []}]},
#          {'6': 
#              [{'7': []},
#              {'18': []}]}]},
#      {'3':
#          [{'4':
#              [{'5': []},
#              {'12': []}]},
#          {'9': 
#              [{'10': []}, 
#              {'27': []}]}]}]}




# ----------------------------------------------------------------------------------------------------------


def F(x, name):
    cnt = 0
    def func(cmb):
        nonlocal cnt
        cnt += 1
        return 10*cmb[0] + x, name + str(cnt) + " " + cmb[1], [*cmb[2], name]

    return func


def gen_bin_tree(h, cmb, f, g):
    return { cmb[1] : [cmb[2], [gen_bin_tree(h-1, F(cmb), f, g) for F in [f, g]] if h else [] ] }

gen_bin_tree(3, (1, "r", []), F(1, 'f'), F(2, 'g'))
