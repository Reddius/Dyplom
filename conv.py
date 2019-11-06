import wave
from scipy import signal
from scipy.io import wavfile
import matplotlib.pyplot as plt
import numpy as np
import simpleaudio as sa

"""
niedziałający
Moduł nakładający odpowiedź impulsową na nagranie

"""

orig = wavfile.read('./data/conv/orig.wav')
ir = wavfile.read('./data/conv/ir.wav')

o = wave.open('./data/conv/orig.wav', 'r')
print("channels: {} sampwidth: {}".format(o.getnchannels(), o.getsampwidth()))

print(orig)
print(ir)

orig = np.array(orig[1], dtype='int16')
orig = orig/max(orig)
ir = np.array(ir[1], dtype='int16')
ir = ir/ max(ir)

new_size = orig.shape[0]-orig.shape[0]%2048
n_chunks = int(new_size/2048)
print(n_chunks)
print(n_chunks*2048)
print(orig.shape[0])
orig = orig[:n_chunks*2048]

convolve = signal.convolve(orig, ir, mode='same')
print(convolve)

chunks = np.split(orig, n_chunks)

new = np.array([])
for chunk in chunks:
    print(new.shape)
    new = np.concatenate((new, signal.convolve(chunk, ir, mode='same')))

print(orig.shape)

plt.subplot(4,1,1)
plt.plot(orig)

plt.subplot(4,1,2)
plt.plot(ir)

plt.subplot(4,1,3)
plt.plot(new)

# new = np.fft.irfft(new)
plt.subplot(4,1,4)
plt.plot(convolve)

plt.show()

# new_file = wave.open("new_file.wav", 'w')
# new_file.setframerate(44100)
# new_file.setsampwidth(2)
# new_file.setnchannels(1)
# new_file.writeframes(new)
#
# new_file.close()


pla_obj = sa.play_buffer(convolve, 1, 2, 44100)
pla_obj.wait_done()

