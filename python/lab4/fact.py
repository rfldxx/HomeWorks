# Battle Royale факториалов

import sys

# изменение глубины рекурсии
sys.setrecursionlimit(100000)

# изменения max размера длинной арифметики
sys.set_int_max_str_digits(100000)


def fact_recursive(n):
    return n * fact_recursive(n-1) if n > 1 else 1

def first_pair_merging(A):
    result = 1
    for x in A:
        result *= x
    return result


import types
def adjacent_pair_merging(A):
    if( not isinstance(A, list) ): A = list(A)

    n = len(A)
    A.append(1)
    while n > 1:
        A[n] = 1
        n = (n+1)//2
        for i in range(n):
            A[i] = A[2*i]*A[2*i+1]
    return  A[0]


import heapq
def min_pair_merging(A):
    if( not isinstance(A, list) ): A = list(A)

    n = len(A)
    heapq.heapify(A)

    for iteration in range(n-1):
        mlt = heapq.heappop(A) * heapq.heappop(A)
        heapq.heappush(A, mlt)
    return A[0]


# Ещё бы попробывать эти "сверкти" захардкодить в функции и сравнить производительность


def fact_classic(n, merging = first_pair_merging):
    return merging( range(1, n+1) )



# я слышал, что для ускорения вычислений, лучше перемножать максимально близкие по размеру числа



from random import shuffle
def fact_classic_1(n, pre_shuffle=1, merging = adjacent_pair_merging):
    A = list(range(1, n+1))
    if( pre_shuffle ): shuffle(A)
    return merging(A)



from math import inf
from collections import deque

def fact3(n):
    # грубое разделение на две области:
    #    значения порядка ~x
    #    значения порядка ~x^2 и более

    A = deque()               # в возрастающем порядке
    B = list(range(n, 0, -1)) # в убыващем порядке
    B.insert(0, inf) # чтобы проще c if-ами было

    for iteration in range(n-1):
        while( len(A) < 2 ):  A.append( B.pop() )

        new_mlt = A.popleft() * A.popleft()

        while( B[-1] < new_mlt ): A.append( B.pop() )

        B.append(new_mlt)

    return B[-1]



def fact3_1(n):
    # Как fact3, только вместо самих чисел, сравниваются их логарифмы
    # (это не дало почти никакого прироста - действительно, наверное у больших чисел навряд ли совпадают разрядности и питон видит что у одного числа больше разрядов и не начинает их сравнивать посимвольно).
    A = deque()
    B = [(x, x.bit_length()) for x in range(n, 0, -1)]
    B.insert(0, (inf, inf)) # чтобы проще c if-ами было

    for iteration in range(n-1):
        while( len(A) < 2 ):  A.append( B.pop() )

        new_mlt = A.popleft()[0]  * A.popleft()[0]
        digits  = new_mlt.bit_length()

        while( B[-1][1] < digits ): A.append( B.pop() )

        B.append( (new_mlt, digits) )

    return B[-1][0]



def fact3_2(n, f):
    # Как fact3_1, только сравнивается не с ln, а с f(ln)
    #    значения порядка ~x
    #    значения порядка ~f(x) и более
    A = deque()
    B = [(x, x.bit_length()) for x in range(n, 0, -1)]
    B.insert(0, (inf, inf)) # чтобы проще c if-ами было

    for iteration in range(n-1):
        while( len(A) < 2 ):  A.append( B.pop() )

        new_mlt = A.popleft()[0]  * A.popleft()[0]
        digits  = new_mlt.bit_length()

        border = f(digits)

        while( B[-1][1] < border ): A.append( B.pop() )

        B.append( (new_mlt, digits) )

    return B[-1][0]



import heapq
def fact5(n, merging = min_pair_merging):
    # Достаем два наименьших числа и возвращаемрезультат их произведения (!а что если читывать повторения чисел!)
    return merging( range(1, n+1) )


def fact6(n, merging = min_pair_merging):
    # Расматривается разложение n! на просте числа
    # Для каждого простого числа находится частота его вхождения и возведение в эту степень с помощью быстого возведения встепень
    # Затем последовательно перемножение степеней простых чисел
    sieve = [0]*(n+1)
    pc = []
    for x in range(2, n+1):
        if sieve[x]: continue
        for y in range(x*x, n+1, x):
            sieve[y] = 1
        cnt = 0
        c = n
        while c:
          c  //= x
          cnt += c

        pc.append((x,cnt))

    return min_pair_merging( pow(x, c) for (x,c) in pc )


def fact6_1(n, merging = min_pair_merging, merging_in_blocks = adjacent_pair_merging):
    # Подобно fact6, только сначала перемножаем все простые числа которые входят одинаковое число раз и потом возводим это произведение в нужную степень.
    sieve = [0]*(n+1)

    L = 0
    pc = [[] for _ in range(n+1)]
    for x in range(2, n+1):
        if sieve[x]: continue
        for y in range(x*x, n+1, x):
            sieve[y] = 1
        cnt = 0
        c = n
        while c:
          c  //= x
          cnt += c

        pc[cnt].append(x)

    heap = []
    for (cnt, A) in enumerate(pc):
        if A != []:
            heap.append( pow(merging_in_blocks(A), cnt) )

    return merging( heap )

