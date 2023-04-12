def iterative_mean():
    n = 0
    s_1 = 0
    s_2 = 0
    mu = lambda : s_1/n
    sigma = lambda : np.sqrt(s_2/n-mu()**2)
    next_val = yield "uwu"
    while True:
        n += 1
        s_1 += next_val
        s_2 += next_val**2
        next_val = yield (mu(),sigma())
