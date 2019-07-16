import matplotlib.pyplot as plt
import numpy as np
from variables import *

def plot_wav(data: list, label: list = "No label",fp = 44100):
    """
rysowanie przebiegu pliku wav w dziedzinie czasu
amplituda znormalizowana

    :param data:    np all_chunks[0] // żeby wszystko na raz trzeba by złączyć all_chunks
    :param fp:           szybkość próbkowania potrzebna do wyliczania osi x (czasu)
    """

    size = len(data)
    plt.title('Analysed files: ')
    for i, file in enumerate(data):
        time = np.linspace(0, len(file)/fp, num=len(file))
        plt.subplot(size, 1, i+1)
        if i >0 :
            plt.plot(time*CHOP, file)
        else:
            plt.plot(time, file)
        plt.xlabel('time (s)')
        if len(label) > i:
            plt.ylabel(label[i])
        else:
            plt.ylabel("No label")

    plt.show()