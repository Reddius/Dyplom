from integral import integrate
from registry import *
from plot import *
import wave
from variables import *


choice = choose_files()
w = wave.open(choice, 'r')

data = list()
label = list()
frames = w.readframes(-1)

frames = np.fromstring(frames, dtype='int16')
frames = frames.astype('float64')
frames = frames/max(frames)

for i, val in enumerate(frames):
    frames[i] = round(val,10)

#frames = np.array([0,1,2,-2,1,-1,3,4,-5,-5,-5,-5,-5])

data.append(frames)
label.append("original sound")


def f(x):
    if np.abs(x) < 1e-10:
        y = x
    else:
        y = x**2
    return y


frames = frames[::CHOP]
f_squared = np.zeros_like(frames)
for i, val in enumerate(frames):
    f_squared[i] = f(val)


data.append(f_squared)
label.append("squared")

f_squared = np.flip(f_squared)

# def F(x):
#     res = np.zeros_like(x)
#     for i, val in enumerate(x):
#         y = quad(f, 0, val)[0]
#         res[i] = y
#     return res
#
# for frame in range(3):
#     print('%d ------> %d' % (frames[frame],F(frames)[frame]))
#
# data.append(F(frames))
integral = integrate(f_squared)
time = np.linspace(0, len(integral)/FP, num=len(integral))


data.append(integral)
label.append("dB energy")

order = integral.argsort()
y = integral[order]
x = time[order]

db30o = x[y.searchsorted(-30, 'left')]
db30 = round(db30o*1000*CHOP)
db0o = x[y.searchsorted(-0.2, 'right')]
db0 = round(db0o*1000*CHOP)
print("0dB---> at: " + str(db0) + "ms")
print("-30dB-> at: " + str(db30) + "ms")
print("-60dB-> at: " + str(db30+(db30-db0)) + "ms [extrapolated]")
print("T30------>: " + str((db30-db0)*2) + "ms")

new = np.zeros_like(integral)
for i, val in enumerate(new):
    new[i] = -60

x1 = int((db30o)*FP)
x2 = int((db0o)*FP)
x3 = int((db0o+((db30o-db0o)*2))*FP)
print(x1)
print(x2)
print(x3)
new[x1] = 1
new[x2] = 1
new[x3] = 1

plot_wav(data, label)
plt.plot(time*6, integral, 'b', time*6, new, 'r--')
plt.xlabel('time (s)')
plt.ylabel("dB")
plt.title("Spadek o 30dB w %dms [dB=0 w %dms] => T30= %dms" % (db30-db0, db0, (db30-db0)*2))
plt.show()

