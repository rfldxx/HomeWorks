# ------------------------------------------------------------------------------
# Тесты
# ------------------------------------------------------------------------------

# from gen_bin_tree import gen_bin_tree

from typing import Callable, Any, List, Tuple

import unittest


class TestGenBinTree(unittest.TestCase):
    def presetFunction(self, lst: List[int], updater: Callable[[int, Any], int] = lambda x, _: x) -> Tuple[Callable[[Any], int], Callable[[Any], None], Callable[[], bool]]:
        """
        Создание функции (`f`) возвращающей элемент из списка lst на основе внутреннего индекса `i`, без повторного доступа к индексу;
        и оберток (`update`, `is_ended`) для контроля этого идекса `i` и проверки были ли все значения списка lst посещены.

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
            if( was[i] ):           raise IndexError(f"re-accessing the index: {i}")
            was[i] = 1

            return lst_copy[i]

        return f, update, is_ended



    def test_by_generating_f_g(self) -> None:
        """
        Рекурсивная проверка, что дерево, сгеннерированое по функциям f и g, действительно имеет эти значения в узлах.
        Функция f - возвращает последовательно чётные значения (начиная с 0), функция g - нечётные.
        Также проверяется что каждая функция (f и g) вызывается ровно (2^height - 1) раз.
        """
        cheked_height = range(0, 10+1)

        def makeArc(f: Callable[[Any], int], update_f: Callable[[Any], None]) -> Callable[[Any], int]:
            """
            Обёртка над f и update_f - пригодная для использования в тестируемой функции gen_bin_tree.

            Returns:
                Функция `F(x)` - функция возвращающая значение f(x) и внешним эффектом update_f().
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
            L = 2**h - 1  # Number of function calls for each f_lst or g_lst
            f_lst = [2 * i     for i in range(L)]  #   четные значения для f
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
