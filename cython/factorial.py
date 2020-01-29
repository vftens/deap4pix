from numba import jit

@jit
def test(x):
    y = 1
    for i in range(1, x+1):
        y *= i
    return y

print(test(25))

