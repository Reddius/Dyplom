import os
from variables import *

def choose_files(curr_dirr):
    '''''
    Odczyt plików w tym samym folderze, co projekt
    '''''
    list_of_files = os.listdir(curr_dirr)
    only_wave_files = list()
    for i, f in enumerate(list_of_files):
        if f.endswith(".wav"):
            only_wave_files.append(f)

    print('*'*15, 'List Of Files','*'*15)
    for i, file in enumerate(only_wave_files):
        print('%d\t->\t%s' % (i, file))


    '''''
    wybór pliku
    '''''

    choice = int(input("\nChoose file: "))
    print('Choosen file: %s' % only_wave_files[choice])

    choice = os.path.join(DIRECTORY, only_wave_files[choice])

    return choice

