import wave
import math
import matplotlib.pyplot as plt
import numpy as np
from numpy.fft import rfft
from scipy.signal.windows import blackmanharris
from pydub import AudioSegment
import audiosegment


from numpy import argmax, arange


class File:
    """
    Pliki wczytywane jako obiekty klasy
    """
    n_frames = -1       #ile klatek
    frames = []         #wartości klatek
    fp = -1             #częstorliwość próbkowania
    length = -1         #długść plików sekundach
    path = ''           #ścieżka do pliku
    label = ''          #label do zapisywania informacji gdy plik był przerobiony
    snr = -1            #wartość SNR
    channels = -1       #liczba kanałów
    kbps = -1           #bitrate w kilobitach na sekundę

    def __init__(self, path, label):
        self.path = path
        self.n_frames, self.fp, self.channels, self.kbps = self.get_parameters()
        self.frames = self.w_read()
        self.length = self.n_frames/self.fp
        self.label = label
        self.snr = self.signaltonoise()

    def get_parameters(self):

        w = wave.open(self.path, 'r')
        framerate = w.getframerate()
        frames = w.getnframes()
        channels = w.getnchannels()
        # sample width jest w bajtach, a my chcemy bity więc *8
        kbps = round((8*w.getsampwidth()*framerate*channels)/1000)
        return frames, framerate, channels, kbps

    def w_read(self):

        w = wave.open(self.path, 'r')
        return w.readframes(-1)

    def show(self):
        print('*'*30)
        print(self.path)
        print('*'*30)
        print('FRAMES: ', self.n_frames)
        print('FP: '+str(self.fp) + 'Hz')
        print('LENGTH: %0.2fs' % self.length)
        print('SNR: ', self.snr)
        print('Channels: ', self.channels)
        print('kbps: ', self.kbps)
        print('*' * 30)


    def signaltonoise(self, axis=0, ddof=0):
        """
To samo co w zwykłej funkcji ale dla całego sygnału, do przetestowania bo
parametr jest bez
        :param axis:
        :param ddof:
        :return:
        """
        a = np.fromstring(self.frames, 'Int16')
       # a = np.asanyarray(a)
        a = a/max(a)
        m = a.mean(axis)
        sd = a.std(axis=axis, ddof=ddof)
        snr = np.where(sd == 0, 0, m / sd)
        snr = float(snr)*10000
        snr = round(snr, 4)
        return abs(snr)
            #np.where(sd == 0, 0, m / sd)

 #   def get_bitrate(self):


def dice(path_to_file: str, size: int = 0.1):
    """
GET CHUNKS
dzieli sygnał na kawalki

    :param path_to_file: path to wave file
    :param size: size of one chunk in seconds
    :return: array2d
    """
    data = list()
    chunks = audiosegment.from_file(path_to_file)
    chunks = chunks.dice(size)
    for chunk in chunks:
        data.append(chunk.to_numpy_array())

    print("Diced %s to %d chunks each %0.1fs" % (path_to_file, len(chunks), size))
    return data


def get_all_chunks(path_to_file: str, size: int = 15) -> list:
    """
funkcja odczytuje cały plik wav a dane zapisuje w tablicy podzielonej na chunk'i

    :param path_to_file:    ścieżka do pliku
    :param size:            rozmiar jednego chunk'a w bajtach nie bitach, czy ramkach
    :return:                zwraca tablicę 2D z danymi podzielonymi na chunk'i
                                chunks = [[pierwszy chunk], [drugi chunk], [ ...]]
    """
    w = wave.open(path_to_file, 'r')        # ramka to dwa bity
    w_frames = w.readframes(-1)
    w_frames = np.fromstring(w_frames, 'Int16')
    frames = w.getnframes()
    size = int(frames/size)
    if size > (len(w_frames)-1)/2:
        size = int((len(w_frames))//3)
        # rozmiar = połowa plk
        print("Too big chunk compared to size of file (changed to: %d)" % size)

    chunks = [w_frames[i:i+size] for i in range(0, len(w_frames), size)]
    print("%s [%d frames (%d bits) saved as %d chunks of size: %d (bits)] " % (path_to_file, (frames), len(w_frames), int(len(chunks)), size))

    return chunks


def plot_wav(data: list, fp):
    """
rysowanie przebiegu pliku wav w dziedzinie czasu
amplituda znormalizowana

    :param data:    np all_chunks[0] // żeby wszystko na raz trzeba by złączyć all_chunks
    :param fp:           szybkość próbkowania potrzebna do wyliczania osi x (czasu)
    """

    size = (len(data)+1)//2
    plt.title('Analysed files: ')
    for i, file in enumerate(data):
        sig = np.fromstring(file.frames, 'Int16')
        sig = sig / sig.max()
        time = np.linspace(0, len(sig)/fp, num=len(sig))
        plt.subplot(size, 2, i+1)
        plt.plot(time, sig)
        plt.xlabel('time (s)')
        plt.ylabel(file.label + "\n" + file.path)

    plt.show()


def get_peak(data):
    """
Peak frequency from signal
    :param data: signal
    :return: peak frequency
    """
    data = data / max(data)
    data = data * blackmanharris(len(data))
    data = abs(rfft(data))

    f_peak = 44100 * argmax(data) / len(data) / 2

    return f_peak


def get_snr(a, axis=0, ddof=0):
    """
Signal to Noise
przemnożone przez 10 000

    :param a: sygnał
    :param axis: deflaut 0
    :param ddof: deflaut 0
    :return: snr
    """
    a = a/max(a)
    m = a.mean(axis)
    sd = a.std(axis=axis, ddof=ddof)
    if sd != 0:
        snr = np.where(sd == 0, 0, m / sd)
    else:
        snr = 0
    snr = float(snr)*10000 #mnożnik 10 000
    snr = round(snr, 4)
    return abs(snr)


def substract(list1: list, list2: list) -> list:
    """
odejmowanie list

    :return: ynik odejmowania (lista)
    """
    delta = list()
    for x in range(min(len(list1), len(list2))):
        delta.append(list1[x]-list2[x])
    return delta
