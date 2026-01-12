# from gen_bin_tree import gen_bin_tree

from typing import Callable, Any, List, Tuple

import unittest


class TestGenBinTree(unittest.TestCase):
    def presetFunction(self, lst: List[int], updater: Callable[[int, Any], int] = lambda x, _: x+1) -> Tuple[Callable[[Any], int], Callable[[Any], None], Callable[[], bool]]:
        """
        Создание функции (`f`) возвращающей элемент из списка lst на основе внутреннего индекса `i`, без повторного доступа к индексу;
        и оберток (`update`, `is_ended`) для контроля этого идекса `i` и проверки были ли все значения списка lst посещены.

        Args:
            lst:     Список значений, которые будут возвращаться в функции `f`. (В самой функции будет храниться копия этого списка.)
            updater: Функция возвращающая обновлённыую позицию (в списке lst) на основе текущей позиции и дополнительного произвольного аргумента.

        Returns:
            A tuple containing:
                f:        Функция которая, внезависимости от аргумента, возвращает lst[i], где `i` - внутренний индекс.
                update:   Функция обновляющая внутренний индекс `i` на основе переданного аргумента.
                is_ended: Булевая функция возвращающая True, если все значения списка lst были посещены.

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
            if( was[i] ):           raise IndexError(f"re-accessing the index: {i}")
            was[i] = 1

            return lst_copy[i]

        return f, update, is_ended



    def test_by_generating_f_g(self) -> None:
        """
        Проверка, что дерево согласуется с обходом в глубину.

        Рекурсивная проверка, что дерево, сгеннерированое по preset-функциям f и g, действительно имеет эти значения в узлах.
        Для этого создаются копии этих preset-функций и значения в дереве сравниваются с значениями скопированных функций в реккурсивном обходе.
        Также проверяется что каждая функция (f и g) вызывается ровно (2^height - 1) раз.

        В тестировании функция f возвращает последовательно чётные значения (начиная с 0), функция g - нечётные.
        Тестируются деревья с высотами из списка cheked_height.
        """
        cheked_height = range(0, 10+1)

        def makeArc(f: Callable[[Any], int], update_f: Callable[[Any], None]) -> Callable[[Any], int]:
            """
            Обёртка над f и update_f - пригодная для использования в тестируемой функции gen_bin_tree.

            Returns:
                Функция `F(x)` - функция возвращающая значение f(x) и внешним эффектом в виде вызова update_f().
            """
            def F(x: Any) -> int:
                result = f(x)
                update_f()
                return result
            return F


        def recurseve_check(expected_value: int, Tree: Dict[int, List[Any]], fg: List[Callable[[int], int]], path: str = "") -> None:
            """
            Рекурсивная проверка значений в узлах дерева.

            Args:
                expected_value: Ожидаемое значение текущего узла.
                Tree:           Текущее поддерево для проверки.
                fg_funcs:       Генераторы ожидаемых значений для потомков: `fg[0](root_value)` - значение для левого потомка, `fg[1](root_value)` - для правого.
                path:           Путь до текущего узла, кодируется спуском от корня дерева:  `L` - переход   в  левого потомка, `R` - в правого.

            Raises:
                AssertionError: "Error in position: {path}" - путь до первого несопадения в рекурсивном обходе.
            """
            (root_value, subTree), = Tree.items()
            self.assertEqual(root_value, expected_value, "Error in position: " + path)

            for i in range(len(subTree)):
                recurseve_check(fg[i](root_value), subTree[i], fg, path + " " + ("LR"[i]))


        for h in cheked_height:
            L = 2**h - 1  # Количество вызовов каждой из функций f и g при создании дерева выстоты h
            f_lst = [2 * i     for i in range(L)]  #   четные значения для f
            g_lst = [2 * i + 1 for i in range(L)]  # нечетные значения для g

            f, update_f, is_ended_f = self.presetFunction(f_lst, lambda i, _: i+1)
            g, update_g, is_ended_g = self.presetFunction(g_lst, lambda i, _: i+1)

            root_value = -1
            Tree = gen_bin_tree(h, root_value, makeArc(f, update_f), makeArc(g, update_g))

            self.assertTrue(is_ended_f(), "Not all f() values used in generation")
            self.assertTrue(is_ended_g(), "Not all g() values used in generation")

            # создание копий функций f и g
            f1, update_f1, is_ended_f1 = self.presetFunction(f_lst, lambda i, _: i+1)
            g1, update_g1, is_ended_g1 = self.presetFunction(g_lst, lambda i, _: i+1)

            recurseve_check(root_value, Tree, [makeArc(f1, update_f1), makeArc(g1, update_g1)])

            self.assertTrue(is_ended_f1(), "Not all f() values used in checking")
            self.assertTrue(is_ended_g1(), "Not all g() values used in checking")



    def test_by_generating_tree_list(self) -> None:
        """
        Проверка, что дерево согласуется с обходом в ширину.
        
        Рекурсивная проверка, что дерево, сгеннерированое по preset-функциям `*FG_positioned`, действительно имеет эти значения в узлах.
        Для этого создаются копии этих preset-функций и значения в дереве сравниваются с значениями скопированных функций в реккурсивном обходе.
        Также проверяется что каждая функция (f и g) вызывается ровно (2^height - 1) раз.

        В тестировании, значения для узлов дерева создаются в виде (0-индексированного) списка `TreeList`.
        Корень дерева имеет значение `TreeList[0]`, любая вершина под индексом `i` имеет левого потомка под индексом `2i+1`, правого `2i+2`.
        
        Функции из `*FG_positioned` выдают значения для левого потомка (`F`) и для правого (`G`) на основе значений из `TreeList`.
         
        Тестируются деревья с высотами из списка cheked_height.
        """
        cheked_height = range(0, 10+1)


        def path_to_indx(position: List[int]) -> int:
            """Преобразует путь в дереве (последовательность 0/1: переход влево/вправо) в нуль-индексированую позицию в порядке обхода в ширину."""
            i = 1
            for e in position:
                i = 2 * i + e
            return i - 1


        def FG_positioned(h: int, f: Callable[[Any], int], g: Callable[[Any], int], share: Callable[[List[bool]], None] = lambda x : None) -> Tuple[Callable[[int], int], Callable[[int], int]]:
            """
            Создает функции `F` и `G` - пригодные для использования в тестируемой функции gen_bin_tree - обёртки над функциями f и g.
            Такая морока нужна, чтобы переданные в gen_bin_tree функции могли отслеживать на каком шаге выполнения рекурсии они находятся.

            Функции `F` и `G` "связанны": их вызовы моделируют рекурсивное передвижение по полному бинарному дереву высоты h - вызовы при переходе в левого / правого потомка при обходев глубину.
            Путь до текущего узла дерева хранится в переменной `position`.

            Каждый вызов  `F()` / `G()` вызывает внутреннюю функицию передвижения в следующую вершину: `transition_to(0)` / `transition_to(1)`.
            При этом `transition_to` после обновления позиции дополнительно вызывает функцию `share(position)`.  
          
             Args:
                h:     Высота полного бинарного действия.
                f:     Функция, ассоциируемая с переходом в  левого потомка.
                g:     Функция, ассоциируемая с переходом в правого потомка.
                share: Функция вызываемая при переходе в новую вершину (каждом вызове `F`, `G`), принмающая путь `position` до новой вершины.

                в  получает текущий путь (позицию) при переходе.
                A callable that receives the current path (position) when a transition occurs.
            
            Returns:
                Функции с общим внутреним состоянием `F(x)` и `G(y)`, возвращающие значения `f(x)` и `g(y)` и внешним эффектом в виде вызова `share(position)`.
            """

            position: List[bool] = []


            def transition_to(which: bool) -> None:
                """
                Переходит в левого (`which == 0`) или в правого (`which == 1`) потомка.
                При этом, если текщее положение это лист дерева, то сначала выполняется подъём вверх по дереву, до первого подъёма по левому ребру.
                """
                nonlocal position
                if( len(position) == h ):
                    # удаляем до первого нуля включительно ( .pop() - удаляет из списка последний элемент и возвращает его )
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
            Рекурсивная проверка значений в узлах дерева.

            Args:
                Tree:             Текущее поддерево для проверки.
                ExpectedTreeList: Список ожидаемых значений в порядке обхода в ширину.
                indx:             Нуль-индексированая позиция значения текущего узла в ExpectedTreeList.
                path:             Путь до текущего узла, кодируется спуском от корня дерева:  `L` - переход   в  левого потомка, `R` - в правого.

            Raises:
                AssertionError: "Error in position: {path}" - путь до первого несопадения в рекурсивном обходе.
            """
            (root_value, subTree), = Tree.items()
            self.assertEqual(root_value, ExpectedTreeList[indx], "Error in position: " + path)

            for i in range(len(subTree)):
                recurseve_check(subTree[i], ExpectedTreeList, 2*indx + i + 1, path + " " + ("LR"[i]))


        for h in cheked_height:
            L = 2**(h+1) - 1           # Общее количество вершин в дереве высоты h.
            TreeList = list(range(L))  # Установка ожидаемых значений в порядке обхода в ширину.

            # Функция `pre_f` возвращает значения из `TreeList` на основе внутреннего индекса.
            # Функция `update_f(position)` делает этот внутрениий индекс равным: `path_to_indx(position)`.
            # Идейно последовательность действий для работы такая:
            #   1. Переходим в узел "L R L L": `update_f([0, 1, 0, 0])`
            #   2. Получаем значения этого узла из TreeList: `pref_f(Any)`
            pre_f, update_f, is_ended_f = self.presetFunction(TreeList, lambda i, p: path_to_indx(p))

            root_value = pre_f(0)

            Tree = gen_bin_tree(h, root_value, *FG_positioned(h, pre_f, pre_f, update_f))
            self.assertTrue(is_ended_f(), "Not all TreeList value's used in generation")

            recurseve_check(Tree, TreeList)



# Запуск тестов в Google Colab
unittest.main(argv=[''], verbosity=2, exit=False)
