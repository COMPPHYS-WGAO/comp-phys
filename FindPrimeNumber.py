'''
    >>> primenum(1, 3)
    [1, 2, 3]
    >>> primenum(10, 15)
    [11, 13]

    python FindPrimeNumber.py -i 2. -n 20.
    
    python -m doctest -v FindPrimeNumber.py


'''

import numpy as np
def primenum(i, n):
    r = np.array(range(int(i), int(n+1)))
    ls = []
    for k in r:
        j = 0
        for a in range(1, int(n+1)):
            if k%a == 0:
                j+=1
        if j <= 2:
            ls.append(k)
    return ls


if __name__ == "__main__":

    import doctest
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', type = float)
    parser.add_argument('-n', type = float)
    args = parser.parse_args()
    x = args.i
    y = args.n
    print 'Prime numbers between', x, 'and', y, 'are', primenum(x, y)
    

