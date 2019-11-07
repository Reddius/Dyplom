from integral import integrate
from registry import *
from plot import *
import wave
from variables import *
from tkinter import filedialog

data = list()
label = list()

def get_path():

    import_file_path = filedialog.askopenfilename()

    return import_file_path


def read_file():
    # choice = choose_files(DIRECTORY)
    w = wave.open(get_path(), 'r')

    frames = w.readframes(-1)

    frames = np.fromstring(frames, dtype='int16')
    frames = frames.astype('float64')
    frames = frames / max(frames)

    for i, val in enumerate(frames):
        frames[i] = round(val, 10)
    return frames


#frames = np.array([0,1,2,-2,1,-1,3,4,-5,-5,-5,-5,-5])

def do_square(square: float) -> float:
    """
    Funkcja odnosi do kwadratu pomijając małe liczby
    :param square: ^2 albo 1e-10 [float]
    :return: float
    """
    if np.abs(square) < 1e-10:  # number too small
        y = square
    else:
        y = square**2
    return y


frames = read_file()

#   lista do  matplotliba
data.append(frames)
label.append("original sound")

#   uproszczenie całkowania - nie trzeba tak dokładnie
frames = frames[::CHOP]
f_squared = np.zeros_like(frames)
for i, val in enumerate(frames):
    f_squared[i] = do_square(val)


data.append(f_squared)
label.append("squared")

#   odrotność - wynika ze wzoru
f_squared = np.flip(f_squared)

#   całka
integral = integrate(f_squared)
time = np.linspace(0, len(integral)/FP, num=len(integral))


data.append(integral)
label.append("dB energy")
#   osie
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

x1 = int((db30o)*FP)                    # spadek  o 30dB
x2 = int((db0o)*FP)                     # odniesienie
x3 = int((db0o+((db30o-db0o)*2))*FP)    # spadek o 60dB szacowany
print(x1)
print(x2)
print(x3)

# czy tablica jest za mała aby pokazać spadek o 60 db
if x3+1>len(integral):
    arrayToSmall = True
else:
    arrayToSmall = False

if arrayToSmall:    # przypadek gdy -60db jest poza wykresem  - ppowiększ tablicę

    new = np.full(x3+1, -60)
    new_integral = np.full_like(new, -60)
    # kopiuj wartości całki
    for i, val in enumerate(integral):
        new_integral[i] = integral[i]
    time = np.linspace(0, len(new_integral) / FP, num=len(new_integral))

else:   # normalny tryb (bez dopasowania wielkośc tablic)
    new = np.full_like(integral, -60)

# naniesione punkty na osi
new[x1] = 1
new[x2] = 1
new[x3] = 1

plot_wav(data, label)


if arrayToSmall:

    plt.plot(time * 6, new_integral, 'b', time * 6, new, 'r--')
else:
    plt.plot(time * 6, integral, 'b', time * 6, new, 'r--')

plt.xlabel('time (s)')
plt.ylabel("dB")
plt.title("Spadek o 30dB w %dms [dB=0 w %dms] => T30= %dms" % (db30-db0, db0, (db30-db0)*2))
plt.show()

