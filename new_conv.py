from scipy.io import wavfile
import matplotlib.pyplot as plt
import numpy as np
import wave
import simpleaudio as sa
from variables import *
import scipy
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

# def timeLine(Y, fp):
#     return np.linspace(0, len(Y)/fp, num=len(Y))


class Signal:
    def __init__(self, file: WaveFile,title: str, timeDomain: bool):
        self.title = title
        self.timedomain = timeDomain
        self.data = file.RAW
        self.fp = file.FRAMERATE

        def timeLine(Y, fp):
            return np.linspace(0, len(Y) / fp, num=len(Y))

        if timeDomain:
            self.time = self.timeLine(self.data, self.fp)
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



# plot(orig_file.RAW, orig_file.FFT_form)
# impulse_response = np.zeros_like(orig_file.FFT_form)
#
# for index, value in enumerate(impulse_response):
#     if index>=len(IR_file.FFT_form):
#         break
#     impulse_response[index] = IR_file.FFT_form[index]
#
# # splot = np.convolve(orig_file.RAW, IR_file.RAW, mode='full')
#
# widmo_splot = orig_file.FFT_form * impulse_response
#
# splot = np.real(np.fft.irfft(widmo_splot))
#
# # plot(orig_file.RAW, splot, widmo_splot)
# plot(splot)

#
"""
najlepsza wersja conv
"""
def nextpow2(L):
    N = 2
    while N < L: N *= 2
    return N


def convolution(x, h):
    L = len(x) - 1  # linear convolution length
    # L = len(h) + len(x) - 1  # linear convolution length
    N = nextpow2(L)

    H = np.fft.rfft(h, N)  # Fourier transform of the impulse
    X = np.fft.rfft(x, N)  # Fourier transform of the input signal
    H = H/max(H)
    X = X/max(X)
    for i, value in enumerate(H):
        if H[i] < 0.1:
            H[i]=1e-10

    Y = X / H  # spectral multiplication
    y = np.fft.irfft(Y)  # time domain again

    y = np.array(y/(max(y)*1.001), dtype='float32')
    return y


IR_inverted = IR_file.RAW/max(IR_file.RAW)

splot = convolution(orig_file.RAW, IR_inverted)

plot(orig_file.RAW,IR_file.RAW,  splot)
#

"""
wavefile działa do zapisuale potem z modułu wave nie da się odczytać
ponoć trzeba użyć ffmpeg
"""

wavfile.write(filename='file.wav', rate=22050, data=np.array(splot, dtype='float32'))
# fp, x = wavfile.read(filename='file.wav')
# print(x)

# new_file = wave.open("file.wav", 'r')
# print(new_file.getparams())
# new_file.close()



"""
próbowałem jeszcze modułem wave ale nie wychodzi
"""


wav_file = wave.open("file2.wav", 'w')

nchannels = 1
sampwidth = 2
framerate = 44100
nframes = len(splot)
comptype = "NONE"
compname = "not compressed"

wav_file.setparams((nchannels,
                    sampwidth,
                    framerate,
                    nframes,
                    comptype,
                    compname
                    ))

import struct

# for value in splot:
#     data = struct.pack('<f', value)
#     wav_file.writeframes(data)
wav_file.writeframes(np.array(splot, dtype='float32'))
wav_file.close()


# wave_obj = sa.WaveObject.from_wave_file("file.wav")
# play_obj = wave_obj.play()
# play_obj.wait_done()

#
# pla_obj = sa.play_buffer(x, 1, 2, fp)
# pla_obj.wait_done()

