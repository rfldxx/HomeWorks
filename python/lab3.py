from typing import Callable, Any, Dict, List

def gen_bin_tree(h: int, r: int, f: Callable[[int], int], g: Callable[[int], int]) -> Dict[int, List]:
    """
    Рекурсивная генерация бинарного дерева высоты h с значением в корне равным r.
    Левый потомок создается с значением в узле равным f(r), правый с значением g(r).

    Args:
        h: Высота дерева. Если h <= 0, возвращается дерево без потомков.
        r: Значение присваемое в текущий узел.
        f: Функция возвращающая значение  левого потомка по значению родителя.
        g: Функция возвращающая значение правого потомка по значению родителя.

    Returns:
        Словарь, представляющий собой бинарное дерево. Ключ - значение в корне бинарного дерева.
        Значение - либо пустой список, либо список из двух бинарных деревьев такого же формата (левого и правого).

    Example:
        >>> gen_bin_tree(2, 1, lambda x: x+1, lambda y: y*3)
        {1: [{2: [{3: []}, {6: []}]}, {3: [{4: []}, {9: []}]}]}
    """

    return { r: [gen_bin_tree(h-1, F(r), f, g) for F in (f, g)] if h > 0 else [] }



# ------------------------------------------------------------------------------
# Тесты
# ------------------------------------------------------------------------------

import unittest


class TestGenBinTree(unittest.TestCase):
    def presetFunction(self, lst: List[int], updater: Callable[[int, Any], int] = lambda x, _: x) -> Tuple[Callable[[Any], int], Callable[[Any], None], Callable[[], bool]]:
        """
        Создание функции (`f`) возвращающей элемент из списка lst на основе внутреннего индекса `i`, без повторного доступа к индексу;
        и оберток (`update`, `is_ended`) для контроля этого идекса `i` и проверки были ли все значения списка lst посещены. повторного доступа к индексу.
        
        Args:
            lst:     Список значений, которые будут возвращаться в функции `f`. (В самой функции будет храниться копия этого списка.)
            updater: Функция возвращающая обновлённыую позицию (в списке lst) на основе текущей позиции и дополнительного произвольного аргумента.

        Returns:
            A tuple containing:
            - f:        Функция которая, внезависимости от аргумента, возвращает lst[i], где `i` - внутренний индекс.
            - update:   Функция обновляющая внутренний индекс `i` на основе переданного аргумента.
            - is_ended: Булевая функция возвращающая True, если все значения списка lst были посещены.

        Raises:
            IndexError: "re-accessing the index: {i}"         - функция `f` пытается повтороно вернуть lst[i].
            IndexError: "index (i={i}) out of bounds (L={L})" - внутрений индекс `i` за границами списка lst (где L = len(lst)).
        """
        i = 0
        lst_copy = lst.copy()
        L = len(lst_copy)
        was = [0] * L

        def update(t: Any = None) -> None:
            nonlocal i
            i = updater(i, t)

        def is_ended() -> bool:
            nonlocal was
            return was == [1] * L

        def f(x: Any) -> int: 
            # емае это по сути просто гетер
            nonlocal i
            if( i < 0 or  L <= i ): raise IndexError(f"index (i={i}) out of bounds (L={L})")
            # if( is_ended() ):     raise IndexError("to many function call's")  # по идеи излишне, так как в этом случае будет was[i]==1
            if( was[i] ):           raise IndexError(f"re-accessing the index: {i}")
            was[i] = 1

            return lst_copy[i]

        return f, update, is_ended





    def test_by_generating_f_g(self) -> None:
        """
        Тест генерации дерева с использованием функций f и g.
        Проверяет корректность построения дерева и использования всех значений.
        """
        
        """
        Tests gen_bin_tree using distinct lists for functions f and g.

        Verifies that all values in the predefined lists for f and g are used exactly once
        during tree generation and subsequent recursive checking.
        """

        def makeArc(f: Callable[[Any], int], update_f: Callable[[Any], None]) -> Callable[[Any], int]:
            """Обертка для функции f, которая обновляет состояние."""
            """
            Wraps a function `f_arg` and its `update_f_arg` to be used in gen_bin_tree.

            Args:
                f_arg: The function to be wrapped.
                update_f_arg: The update function associated with `f_arg`.

            Returns:
                A new function that calls `f_arg` and then `update_f_arg`.
            """
            def Arcf(x: Any) -> int:
                """Wrapped function that calls f_arg and then updates its state."""
                r = f(x)
                update_f()
                return r
            return Arcf


        def recurseve_check(expected_value: int, Tree: Dict[int, List[Any]], fg: List[Callable[[int], int]], path: str = "") -> None:
            """
            Рекурсивно проверяет корректность дерева.
            
            Параметры:
            ----------
            expected_value : Any
                Ожидаемое значение в текущем узле.
            tree : Dict
                Проверяемое поддерево.
            fg : List[Callable]
                Список функций [f, g] для вычисления потомков.
            path : str
                Строковое представление пути от корня (для отладки).
            """
            """
            Recursively checks the generated tree structure and values.

            Args:
                expected_value: The expected value of the current node.
                Tree: The current subtree to check.
                fg_funcs: A list containing the f and g functions used to generate child values.
                path: A string representing the path to the current node (for error messages).

            Raises:
                AssertionError: If a node's value does not match the expected_value.
            """
            (root_value, subTree), = Tree.items()
            self.assertEqual(root_value, expected_value, "Error in position: " + path)
            
            for i in range(len(subTree)):
                recurseve_check(fg[i](root_value), subTree[i], fg, path + " " + ("LR"[i]))
              

        for h in range(0, 10 + 1):
            L = 2**h - 1  # Number of function calls for each f_lst or g_lst
            f_lst = [2 * i for i in range(L)]      # четные значения для f
            g_lst = [2 * i + 1 for i in range(L)]  # нечетные значения для g
            
            f, update_f, is_ended_f = self.presetFunction(f_lst, lambda i, _: i+1)
            g, update_g, is_ended_g = self.presetFunction(g_lst, lambda i, _: i+1)

            root_value = -1
            Tree = gen_bin_tree(h, root_value, makeArc(f, update_f), makeArc(g, update_g))
            
            self.assertTrue(is_ended_f(), "Not all f() values used in generation")
            self.assertTrue(is_ended_g(), "Not all g() values used in generation")

            # Проверка корректности дерева
            f1, update_f1, is_ended_f1 = self.presetFunction(f_lst, lambda i, _: i+1)
            g1, update_g1, is_ended_g1 = self.presetFunction(g_lst, lambda i, _: i+1)
            
            recurseve_check(root_value, Tree, [makeArc(f1, update_f1), makeArc(g1, update_g1)])
            
            self.assertTrue(is_ended_f1(), "Not all f() values used in checking")
            self.assertTrue(is_ended_g1(), "Not all g() values used in checking")








    def test_by_generating_tree_list(self) -> None:
        """
        Тест генерации дерева на основе списка значений.
        Проверяет соответствие структуры дерева ожидаемым значениям.
        """
        """
        Tests gen_bin_tree by generating a tree where node values correspond to indices
        in a flattened list representation of a complete binary tree.

        Verifies that the generated tree structure and node values match the expected
        linear list.
        """

        def path_to_indx(position: List[int]) -> int:
            """Преобразует путь в дереве в индекс в списке значений."""
            """
            Converts a path (sequence of 0s for left, 1s for right) to a 0-based index
            in a complete binary tree (e.g., array representation).
            Root is at index 0. Left child of node `i` is `2*i+1`, right child is `2*i+2`.

            Args:
                position: A list of integers (0 or 1) representing the path from the root.

            Returns:
                The 0-based index of the node in a complete binary tree.
            """
            i = 1
            for e in position:
                i = 2 * i + e
            return i - 1
         
        def FG_positioned(h: int, f: Callable[[Any], int], g: Callable[[Any], int], share: Callable[[List[int]], None] = lambda x : None) -> Tuple[Callable[[int], int], Callable[[int], int]]:
            """
            Создает функции F и G, которые отслеживают позицию в дереве.
            
            Параметры:
            ----------
            h : int
                Высота дерева.
            f : Callable
                Исходная функция для вычисления значений.
            g : Callable
                Исходная функция для вычисления значений.
            share : Callable
                Функция для передачи текущей позиции.
            
            Возвращает:
            -----------
            tuple
                Кортеж из двух функций (F, G) с отслеживанием позиции.
            """
            """
            Creates wrapper functions F and G that track their position in the tree
            and call the provided `f_arg` and `g_arg`.

            Args:
                h: The maximum height of the tree.
                f_arg: The base function for the left child.
                g_arg: The base function for the right child.
                share: A callable that receives the current path (position) when a transition occurs.

            Returns:
                A tuple containing the wrapped F and G functions.
            """
            position: List[int] = []

            def transition_to(which: int) -> None:
                nonlocal position
                if len(position) == h:
                    # Удаляем элементы до первого нуля включительно
                    while position.pop():
                        pass
                position.append(which)
                share(position)  # Передаем текущую позицию

            def transition_to(which: int) -> None:
                """
                Updates the current `position` list based on the child being generated.
                This function simulates moving up and down the tree to reflect the current
                path of generation.

                Args:
                    which: 0 for left child, 1 for right child.
                """
                nonlocal position
                # If the current branch has reached maximum height, we need to backtrack
                # up the tree to find the next available spot (e.g., a sibling or an ancestor's child).
                if( len(position) == h ):
                    # удаляем до первого нуля включительно ( .pop() - удаляет из списка последний элемент и  возвращает его )
                    while( position.pop() ): pass 

                position.append( which )
                share( position )  # никаких гетеров / сеттеров

            def F(x: Any) -> int:
                transition_to(0)
                return f(x)

            def G(x: Any) -> int:
                transition_to(1)
                return g(x)

            return F, G



    

        def recurseve_check(Tree: Dict[int, List[Any]], ExpectedTreeList: List[int], indx: int = 0, path: str = "") -> None:
            """
            Рекурсивно проверяет значения узлов дерева.
            
            Параметры:
            ----------
            indx : int
                Текущий индекс в представлении дерева массивом.
            tree : Dict
                Проверяемое поддерево.
            expected_tree_list : List[Any]
                Список ожидаемых значений в порядке обхода в ширину.
            path : str
                Строковое представление пути от корня (для отладки).
            """
            """
            Recursively checks the generated tree against a flattened list of expected values.

            Args:
                Tree: The current subtree to check.
                ExpectedTreeList: The flattened list of all expected node values (0-indexed).
                indx: The 0-based index of the current node in ExpectedTreeList.
                path: A string representing the path to the current node (for error messages).

            Raises:
                AssertionError: If a node's value does not match the expected value from ExpectedTreeList.
            """
            (root_value, subTree), = Tree.items()
            self.assertEqual(root_value, ExpectedTreeList[indx], "Error in position: " + path)

            for i in range(len(subTree)):
                recurseve_check(subTree[i], ExpectedTreeList, 2*indx + i + 1, path + " " + ("LR"[i]))

       

        for h in range(0, 10+1):
            L = 2**(h+1) - 1 # Total number of nodes in a complete binary tree of height h
            TreeList = list(range(L))

            # presetFunction creates a callable `pre_f` that returns values from `TreeList`
            # based on an internal index. `update_f` modifies this internal index by mapping
            # the current path `p` to an index in `TreeList` using `path_to_indx`.
            pre_f, update_f, is_ended_f = self.presetFunction(TreeList, lambda i, p: path_to_indx(p))

            # To get the root_value, we first need to set the internal index of `pre_f`
            # to the index corresponding to the root's path (which is an empty list []).
            root_path: List[int] = []
            update_f(root_path) # Sets pre_f's internal index to 0
            root_value = pre_f(0) # Gets the value for the root (TreeList[0])

            # Generate the binary tree using `pre_f` for both left and right branches,
            # and `update_f` to track the current position during generation.
            Tree = gen_bin_tree(h, root_value, *FG_positioned(h, pre_f, pre_f, update_f))
            self.assertTrue(is_ended_f(), "Not all TreeList value's used in generation")

            recurseve_check(Tree, TreeList)




# Запуск тестов в Google Colab
unittest.main(argv=[''], verbosity=2, exit=False)
