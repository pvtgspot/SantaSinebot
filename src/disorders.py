import random

def D(n):
    if n <= 1:
        return 0

    return n * D(n - 1) + pow(-1, n)


# в 20 процентах случаев присутствуют циклы
def disorder(xs):
    n = len(xs)
    a = xs.copy()
    u = n
    mark = [False] * len(xs)
    i = n - 1
    while u >= 2:
        if not mark[i]:
            j = random.randint(0, i - 1)            
            while mark[j]:
                j = random.randint(0, i - 1)

            a[i], a[j] = a[j], a[i]
            p = random.uniform(0, 1)
            if p < (u - 1) * D(u - 2) / D(u):
                mark[j] = True
                u -= 1
            u -= 1
        i -= 1
    return a
