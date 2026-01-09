### В ПРОЦЕССЕ . . .


def gen_bin_tree(h, r, f, g):
    return { r : [gen_bin_tree(h-1, F(r), f, g) for F in [f, g]] if h > 0 else [] }

import unittest

class TestGenBinTree(unittest.TestCase):
    def test_by_generating_f_g(self) -> None:
        def presetFunction(lst):
            i = 0
            lst_copy = lst.copy()
            def is_ended():
                nonlocal i
                return   i >= len(lst_copy)

            def f(x):
                nonlocal i
                if( is_ended() ): raise IndexError("to many function call's")
                # делаем аналог return lst_copy[i++] из C++
                i += 1
                return lst_copy[i-1]
            return f, is_ended


        def recurseve_check(expected_value, Tree, fg, path = ""):
            (root_value, subTree), = Tree.items()
            self.assertEqual(root_value, expected_value, "Error in position:" + path)
            
            for i in range(len(subTree)):
                recurseve_check(fg[i](root_value), subTree[i], fg, path + " " + ("LR"[i]))
        

        for h in range(0, 10+1):
            L = 2**h - 1
            f_lst = [ 2*i   for i in range(L) ]  #   чётные 
            g_lst = [ 2*i+1 for i in range(L) ]  # нечётные 
            f, is_ended_f = presetFunction(f_lst)
            g, is_ended_g = presetFunction(g_lst)

            root_value = -1
            Tree = gen_bin_tree(h, root_value, f, g)
            self.assertTrue(is_ended_f(), "Not all f() value's used in generation")
            self.assertTrue(is_ended_g(), "Not all g() value's used in generation")

            # printTree(Tree)
            f1, is_ended_f1 = presetFunction(f_lst)
            g1, is_ended_g1 = presetFunction(g_lst)
            recurseve_check(root_value, Tree, [f1, g1])
            self.assertTrue(is_ended_f1(), "Not all f() value's used in checking")
            self.assertTrue(is_ended_g1(), "Not all g() value's used in checking")

            
    def test_by_generating_tree_list(self) -> None:
        def presetFW(lst):
            i = 0
            lst_copy = lst.copy()

            def writer(position):
                nonlocal i
                i = 1
                for e in position:
                    i = 2*i + e

            def f(r):
                nonlocal i
                return lst_copy[i]
            
            return f, writer


        def FG_positioned(h, f, g, writer = lambda x : None):
            position = []

            def add(which):
                nonlocal position
                if( len(position) == h ):
                    # удаляем до первого нуля включительно ( .pop() - удаляет из списка последний элемент и  возвращает его )
                    while( position.pop() ): pass 

                position.append( which )
                writer(position)

            def F(r):
                add(0)
                return f(r)

            def G(r):
                add(1)
                return g(r)

            return F, G


        
        def recurseve_check(indx, Tree, ExpectedTreeList, path = ""):
            (root_value, subTree), = Tree.items()
            self.assertEqual(root_value, ExpectedTreeList[indx], "Error in position:" + path)
            
            for i in range(len(subTree)):
                recurseve_check(2*indx+i, subTree[i], ExpectedTreeList, path + " " + ("LR"[i]))


        for h in range(0, 10+1):
            L = 2**(h+1) - 1
            TreeList = list(range(L+1))

            f, writer = presetFW(TreeList)
            Tree = gen_bin_tree(h, TreeList[1], *FG_positioned(h, f, f, writer))
            
            recurseve_check(1, Tree, TreeList)





# Запуск тестов в Google Colab
unittest.main(argv=[''], verbosity=2, exit=False)
