# ФИО: Хузин Рафаэль Илнурович
# группа: P4150

# ЛАБОРАТОРНАЯ РАБОТА 1.  СУММА ДВУХ
# Дан массив целых чисел nums и целочисленное значение переменной target, верните индексы двух чисел таким образом, 
# чтобы они в сумме давали target. 
# 
# У каждого входного набора может не быть решений и может быть только одно решение, если есть элементы дающие в сумме target. 
# Вы не можете использовать один и тот же элемент дважды (и соответственно индекс тоже).
# Вы можете вернуть ответ в любом порядке нахождения индексов.

def f(a, target):
    aa = sorted( (x, indx) for (indx, x) in enumerate(a) )

    j = len(a) - 1
    for i, (x, indx) in enumerate(aa):
        while( i < j and x + aa[j][0] > target ): j -= 1

        if( i == j ): break
        if( x + aa[j][0] == target ): return [indx, aa[j][1]]

    return []

print( f([2, 7, 11, 15], 9) )  # Output: [0, 1]
print( f([3, 2, 4], 6) )       # Output: [1, 2]
print( f([3, 3], 6) )          # Output: [0, 1]

print( f([3, 3], 3) )          # Output: []
print( f([3], 3) )             # Output: []
print( f([ ], 3) )             # Output: []

# можно оттестировать здесь: https://leetcode.com/problems/two-sum/description/
