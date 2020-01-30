from scipy.integrate import *
import numpy as np
import math


def integrate(f):
    integral = np.zeros_like(f)

    ox = range(len(f))

    print("wait - calculating integral - {} samples".format(len(f)))

    for i in range(1, len(f)):
        y = simps(f[0:i], ox[0:i])
        integral[len(f)-i] = y
    print("done")
    #db
    integral_max=max(integral)
    for i, val in enumerate(integral):
        if val > 1e-10:
            s = val / integral_max
            l = math.log10(s)
            integral[i] = 10 * l
        else:
            integral[i] = -80
    return integral
