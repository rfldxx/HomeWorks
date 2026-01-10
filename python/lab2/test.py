# ------------------------------------------------------------------------------
# Тесты
# ------------------------------------------------------------------------------

# from guess_number import guess_number

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
