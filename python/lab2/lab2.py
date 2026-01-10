# ЛАБОРАТОРНАЯ РАБОТА 2.  УГАДАЙ ЧИСЛО
# Реализуйте программно классическую простую игру "угадай число" (guess number) с помощью алгоритма медленного перебора (инкремента) по одному числа, либо с помощью алгоритма бинарного поиска.
# Алгоритм принимает на вход само число, которое он должен угадать, интервал значений в котором оно загадано и в цикле делает угадывания тем или иным выбранным вами способом.
# После угадывания из функции алгоритма возвращается угаданное число и число угадываний/сравнений, которые пришлось проделать.
# Обязательно напишите хорошую документацию (см. PEP-257) к своему коду. Используйте подсказки по аннотации типов (документация, шпаргалка по типам).
# 
# Напишите тесты с помощью unittest и удостоверьтесь, что ваше решение их проходит. 
# 
# При вызове функции guess_number на вход она должна получать число, список, внутри которого происходит угадывание искомого числа (список может быть не отсортирован, не содержит повторяющихся значений),
# способ угадывания (медленный перебор или алгоритм бинарного поиска).
# Эта функция должна вернуть кортеж или список с двумя значениями, искомым числом и количеством угадываний. 
# 
# Список для угадывания формируется как list(range(начало_диапазона, конец_диапазона + 1)). В дополнение к этому предлагается написать вспомогательную (helper) функцию для формирования значений с клавиатуры.


from typing import Tuple, List, Callable

def solver_gate(l : int, r : int, x : int, ask : Callable[[int], bool]) -> Tuple[int, int]:
    """
    Переходит от диапазона (l, r) к новому диапазону в зависимости от результата ask(x).
    Если ask(x) == 0, то новый диапазон: (l, x).
    Если ask(x) == 1, то новый диапазон: (x+1, r).
    """
    return ( (l, x), (x+1, r) )[ ask(x) ]

def seq_x(l : int, r : int) -> int:
    """
    Возвращает индекс к которому делается запрос в игре guess_number,
    при последовательном поиске, если загадываемое число находится в диапазоне (l, r).
    """
    return l

def bin_x(l : int, r : int) -> int:
    """
    Возвращает индекс к которому делается запрос в игре guess_number,
    при бинарном поиске, если загадываемое число находится в диапазоне (l, r).
    """
    return (l+r)//2

def guess_number(target : int, lst : List[int], type : str = 'seq') -> Tuple[int, int]:
    """
    Угадывает число target в списке lst с использованием указанного алгоритма поиска type ('bin' / 'seq').
    Рассматривается игра с запросами вида: "загаданное число больше x?".
    
    Args:
        target: Число, которое требуется угадать
        lst: Список целых чисел для поиска
        search_type: Тип алгоритма поиска:
                   'seq' - последовательный поиск
                   'bin' - бинарный поиск
    
    Returns:
        Кортеж (угаданное_число, количество_попыток)
    """
    sorted_lst = sorted( lst )

    def kernel(l : int, r : int) -> Tuple[int, int]: 
        x = (bin_x, seq_x)[type=='seq'](l, r)
        return solver_gate(l, r, x, lambda i: target > sorted_lst[i])

    cnt  = 0
    l, r = 0, len(sorted_lst)-1
    while( l != r ):
        l, r = kernel(l, r)
        cnt += 1

    return sorted_lst[l], cnt





# ------------------------------------------------------------------------------
# Тесты
# ------------------------------------------------------------------------------
import unittest
import itertools

class TestGuessNumber(unittest.TestCase):
    def test_bin_return(self) -> None:
        """
        Проверка бинарного поиска на каждом загаданном target из чисел: [shift, shift+1, ..., shift+n).
        Должно найтись число равное target.
        Число запросов cnt должно удовлетворять: floor(ln_2(n)) <= cnt <= ceil(ln_2(n)).
        """
        def expected_diap(n : int) -> Tuple[int, int]:
            l = 0
            while( 2**(l+1) < n ): l += 1
            r = l + (2**l != n)
            return l, r

        nn     = [1, 2, 3, 4, 5, 10, 1000]
        shifts = [-10**9, -3, -2, -1, 0, 1, 2, 3, 10**9]
        for n, shift in itertools.product(nn, shifts):
            for i in range(n):
                lst = list(range(shift, shift+n))
                target = shift + i
                num, cnt = guess_number(target, lst, 'bin')
                self.assertEqual(num, target)
                l, r = expected_diap(n)
                self.assertLessEqual(l, cnt)
                self.assertLessEqual(cnt, r)


    def test_seq_return(self) -> None:
        """
        Проверка последовательного поиска на каждом загаданном target из чисел: [shift, shift+1, ..., shift+n).
        Должно найтись число равное target.
        Число запросов cnt должно удовлетворять: cnt == min( target-shift+1, n-1 ).
        """
        nn     = [1, 2, 3, 4, 5, 10, 1000]
        shifts = [-10**9, -3, -2, -1, 0, 1, 2, 3, 10**9]
        for n, shift in itertools.product(nn, shifts):
            for i in range(n):
                lst = list(range(shift, shift+n))
                target = shift + i
                num, cnt = guess_number(target, lst, 'seq')
                self.assertEqual(num, target)
                # expected_cnt = i + (i != n-1)
                expected_cnt = min( i+1, n-1 )
                self.assertEqual(cnt, expected_cnt)


# Запуск тестов в Google Colab
unittest.main(argv=[''], verbosity=2, exit=False)
