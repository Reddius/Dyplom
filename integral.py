from scipy.integrate import *
import numpy as np
import math


def integrate(f):
    integral = np.zeros_like(f)

    ox = range(len(f))

    print("wait - calculating integral - {} samples".format(len(f)))

    # tylko debug=========================================
    temp = -1
    for i in range(1, len(f)):
        progress = round(i / len(f) * 100);
        if progress % 10 == 0 and temp !=progress:
            print("{}%".format(round(i / len(f) * 100)))
            temp = progress
    #===================================================

        # print(round((i/len(f_squared))*100), "%")
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
