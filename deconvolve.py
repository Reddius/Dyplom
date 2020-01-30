from scipy.io import wavfile
import matplotlib.pyplot as plt
import numpy as np
import wave
import simpleaudio as sa
from variables import *
from scipy.signal import deconvolve
"""
Moduł nakładający odpowiedź impulsową na nagranie

"""

#
# orig = wavfile.read('./data/conv/orig.wav')
# ir = wavfile.read('./data/conv/ir.wav')


# o = wave.open('./data/conv/orig.wav', 'r')


class WaveFile:
    PATH = str()

    def __init__(self, path):
        self.PATH = path
        self.FILE = wave.open(self.PATH)
        [self.CHANNELS, self.SAMP_WIDTH, self.FRAMERATE, self.NFRAMES, *self.rest] = self.FILE.getparams()
        self.RAW = np.fromstring(self.FILE.readframes(-1), dtype='int32')
        self.RAW = self.RAW/max(self.RAW)
        self.FFT_form = self.fft()
        print("FILE: {}".format(self.PATH))
        print("\t\tchannels: {} sampwidth: {} framerate: {}".format(self.CHANNELS, self.SAMP_WIDTH, self.FRAMERATE))

    def fft(self):
        return np.fft.rfft(self.RAW)

    def ifft(self):
        return np.fft.irfft(self.FFT_form)


def plot(toPlot, *args):

    print(len(args))
    N_PLOTS = 1 + len(args)

    plt.subplot(N_PLOTS, 1, 1)
    plt.plot(timeLine(toPlot, 44100),toPlot)

    for index, pl in enumerate(args):

        plt.subplot(N_PLOTS, 1, index+2)
        plt.plot(pl)

    plt.show()

def timeLine(Y, fp):
    return np.linspace(0, len(Y)/fp, num=len(Y))


class Signal:
    def __init__(self, file: WaveFile,title: str, timeDomain: bool):
        self.title = title
        self.timedomain = timeDomain
        self.data = file.RAW
        self.fp = file.FRAMERATE
        if timeDomain:
            self.time = timeLine(self.data, self.fp)
        else:
            self.time = -1


def plot_signals(*args: Signal):

    for i, arg in enumerate(args):
        plt.subplot(len(args),1, i+1)
        plt.title(arg.title)
        if arg.timedomain:
            plt.xlabel('time [s]')
            plt.plot(arg.time, arg.data)
        else:
            plt.plot(arg.data)
            plt.xlabel('frequency [Hz]')
    plt.show()


orig_file = WaveFile(ORIG)
IR_file = WaveFile(IR)

sig_1 = Signal(file=orig_file,
               title="Original file",
               timeDomain=True)
sig_2 = Signal(file=IR_file,
               title="Impulse response",
               timeDomain=True)

plot_signals(sig_1, sig_2)

def nextpow2(L):
    N = 2
    while N < L: N *= 2
    return N

deconv, _= deconvolve(orig_file.RAW, IR_file.RAW)
plt.plot(deconv)
plt.show()


# plot(orig_file.RAW,IR_file.RAW,  deconv)

wavfile.write(filename='deconv.wav', rate=22050, data=np.array(deconv, dtype='float32'))