# Battle Royale

from operator import ipow
# Battle Royale факториалов

def fact_recursive(n):
    return n * fact_recursive(n-1) if n > 1 else 1

  
def fact_classic(n):
    r = 1
    for x in range(1, n+1):
        r *= x
    return r

# from random import shuffle
def fact_classic_1(n):
    r = 1
    A = list(range(1, n+1))
    A.append(1) # для удобства
    # shuffle(A)
    # print(n, A)
    while n > 1:
        if( n%2 ): 
            A[n] = 1
            n += 1
        for i in range(n//2):
            A[i] = A[2*i]*A[2*i+1]
        n = n//2
    return A[0]



from math import inf
from collections import deque

def fact3(n):
    # грубое разделение на две области:
    #    значения порядка ~x
    #    значения порядка ~x^2 и более

    A = deque()
    B = list(range(n, 0, -1))
    B.insert(0, inf) # чтобы проще c if-ами было

    # print(B)

    for iteration in range(n-1):
        while( len(A) < 2 ):  A.append( B.pop() )

        new_mlt = A.popleft()  * A.popleft() 

        while( B[-1] < new_mlt ): A.append( B.pop() )

        B.append(new_mlt)


    return B[-1]

def fact3_1(n):
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



def fact4(n, f):
    # грубое разделение на две области:
    #    значения порядка ~x
    #    значения порядка ~f(x) и более
    A = deque()
    B = [(x, x.bit_length()) for x in range(n, 0, -1)]
    B.insert(0, (inf, inf)) # чтобы проще c if-ами было

    # print(B)

    for iteration in range(n-1):
        while( len(A) < 2 ):  A.append( B.pop() )

        new_mlt = A.popleft()[0]  * A.popleft()[0]
        digits  = new_mlt.bit_length()

        border = f(digits)

        while( B[-1][1] < border ): A.append( B.pop() )

        B.append( (new_mlt, digits) )


    return B[-1][0]



import heapq
def fact5(n):
    heap = [x for x in range(1, n+1)]
    heapq.heapify(heap)

    for iteration in range(n-1):
        mlt = heapq.heappop(heap) * heapq.heappop(heap)
        heapq.heappush(heap, mlt)
    return heap[0]


def fact6(n):
    sieve = [0]*(n+1)
    pc = []
    for x in range(2, n):
        if sieve[x]: continue
        for y in range(x*x, n, x):
            sieve[y] = 1
        cnt = 0
        c = n
        while c:
          c  //= x
          cnt += c
        
        pc.append((x,cnt))

    heap = [pow(x, c) for (x,c) in pc]
    heapq.heapify(heap)
    L = len(pc)

    for iteration in range(L-1):
        mlt = heapq.heappop(heap) * heapq.heappop(heap)
        heapq.heappush(heap, mlt)
    return heap[0]


def fact6_1(n):
    sieve = [0]*(n+1)

    L = 0
    pc = [[] for _ in range(n+1)]
    for x in range(2, n+1):
        if sieve[x]: continue
        for y in range(x*x, n, x):
            sieve[y] = 1
        cnt = 0
        c = n
        while c:
          c  //= x
          cnt += c
        
        pc[cnt].append(x)

    heap = []
    i = 0
    for (k, A) in enumerate(pc):
          if A == []: continue
          l = len(A)
          A.append(1)
          while l > 1:
              if( l%2 ): 
                  A[l] = 1
                  l += 1
              for i in range(l//2):
                  A[i] = A[2*i]*A[2*i+1]
              l = l//2

          heap.append( pow(A[0], k) )
          i += 1

    heapq.heapify(heap)
    L = len(heap)

    for iteration in range(L-1):
        mlt = heapq.heappop(heap) * heapq.heappop(heap)
        heapq.heappush(heap, mlt)
    return heap[0]



 

import timeit
def check(f, n, num_runs = 100):
    t = timeit.timeit(lambda: f(n), number=num_runs) / num_runs
    print("t =", t, "for val", n)

from functools import partial

a = 20000
check(fact_recursive, a)                     # t = 0.11220435719000306  for val 20000

check(fact_classic, a)                       # t = 0.10875383063999834  for val 20000
check(fact_classic_1, a)                     # t = 0.01967309137000484  for val 20000

check(fact3, a)                              # t = 0.02237139875000139  for val 20000
check(fact3_1, a)                            # t = 0.02788334269000188  for val 20000

check(partial(fact4, f=lambda x: x//2), a)   # t = 0.03036437675000343  for val 20000
check(partial(fact4, f=lambda x: x), a)      # t = 0.04168494952000401  for val 20000
check(partial(fact4, f=lambda x: 3*x//2), a) # t = 0.030536252680012695 for val 20000
check(partial(fact4, f=lambda x: 2*x), a)    # t = 0.030665910860006987 for val 20000

check(fact5, a)                              # t = 0.035707068629999415 for val 20000
check(fact6, a)                              # t = 0.028582149750000098 for val 20000
check(fact6_1, a)                            # t = 0.02037144067000554  for val 20000
