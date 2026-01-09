### В ПРОЦЕССЕ . . .

def gen_bin_tree(h, r, f, g):
    return { r : [gen_bin_tree(h-1, F(r), f, g) for F in [f, g]] if h > 0 else [] }



# ------------------------------------------------------------------------------
# Тесты
# ------------------------------------------------------------------------------


import unittest

class TestGenBinTree(unittest.TestCase):
    def presetFunction(self, lst, updater = lambda _ : None):
            i = 0
            lst_copy = lst.copy()
            L = len(lst_copy)
            was = [0] * L

            def update(t = None):
                nonlocal i
                i = updater(i, t)

            def is_ended():
                nonlocal was
                return   was == [1] * L

            def f(x):
                nonlocal i
                if( i < 0 or  L <= i ): raise IndexError("index (i=" + str(i) + ") out of bounds (L=" + str(L) + ")")
                # if( is_ended() ):     raise IndexError("to many function call's")  # по идеи излишне, так как в этом случае будет was[i]==1
                if( was[i] ):           raise IndexError("re-accessing the index: " + str(i))
                was[i] = 1

                return lst_copy[i]
            return f, update, is_ended


    def test_by_generating_f_g(self) -> None:
        def makeArc(f, update_f):
            def Arcf(x):
                r = f(x)
                update_f()
                return r
            return Arcf

        def recurseve_check(expected_value, Tree, fg, path = ""):
            (root_value, subTree), = Tree.items()
            self.assertEqual(root_value, expected_value, "Error in position:" + path)
            
            for i in range(len(subTree)):
                recurseve_check(fg[i](root_value), subTree[i], fg, path + " " + ("LR"[i]))
        
        for h in range(0, 10+1):
            L = 2**h - 1
            f_lst = [ 2*i   for i in range(L) ]  #   чётные 
            g_lst = [ 2*i+1 for i in range(L) ]  # нечётные 
            f, update_f, is_ended_f = self.presetFunction(f_lst, lambda i, _ : i+1)
            g, update_g, is_ended_g = self.presetFunction(g_lst, lambda i, _ : i+1)

            root_value = -1
            Tree = gen_bin_tree(h, root_value, makeArc(f, update_f), makeArc(g, update_g))
            self.assertTrue(is_ended_f(), "Not all f() value's used in generation")
            self.assertTrue(is_ended_g(), "Not all g() value's used in generation")

            # printTree(Tree)
            f1, update_f1, is_ended_f1 = self.presetFunction(f_lst, lambda i, _ : i+1)
            g1, update_g1, is_ended_g1 = self.presetFunction(g_lst, lambda i, _ : i+1)
            recurseve_check(root_value, Tree, [makeArc(f1, update_f1), makeArc(g1, update_g1)])
            self.assertTrue(is_ended_f1(), "Not all f() value's used in checking")
            self.assertTrue(is_ended_g1(), "Not all g() value's used in checking")


    def test_by_generating_tree_list(self) -> None:          
        def path_to_indx(position):
            i = 1
            for e in position:
                i = 2*i + e
            return i-1
        
        def FG_positioned(h, f, g, share = lambda x : None):
            position = []

            def transition_to(which):
                nonlocal position
                if( len(position) == h ):
                    # удаляем до первого нуля включительно ( .pop() - удаляет из списка последний элемент и  возвращает его )
                    while( position.pop() ): pass 

                position.append( which )
                share( position )  # никаких гетеров / сеттеров

            def F(x):
                transition_to(0)
                return f(x)

            def G(x):
                transition_to(1)
                return g(x)

            return F, G
        
        def recurseve_check(indx, Tree, ExpectedTreeList, path = ""):
            (root_value, subTree), = Tree.items()
            self.assertEqual(root_value, ExpectedTreeList[indx-1], "Error in position:" + path)
            
            for i in range(len(subTree)):
                recurseve_check(2*indx+i, subTree[i], ExpectedTreeList, path + " " + ("LR"[i]))

        for h in range(0, 10+1):
            L = 2**(h+1) - 1
            TreeList = list(range(L))

            pre_f, update_f, is_ended_f = self.presetFunction(TreeList, lambda _, p: path_to_indx(p))

            root_value = pre_f(0)
            Tree = gen_bin_tree(h, root_value, *FG_positioned(h, pre_f, pre_f, update_f))
            self.assertTrue(is_ended_f(), "Not all TreeList value's used in generation")
            
            recurseve_check(1, Tree, TreeList)


# Запуск тестов в Google Colab
unittest.main(argv=[''], verbosity=2, exit=False)
