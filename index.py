import wave
from variables import *
from registry import choose_files
import os


class Data:
    file = 'Empty'
    t60 = None
    colour = None

    def choose_file(self):
        '''''
        Odczyt plików w tym samym folderze, co projekt
        '''''
        list_of_files = os.listdir(DIRECTORY)
        only_wave_files = list()
        for i, f in enumerate(list_of_files):
            if f.endswith(".wav"):
                only_wave_files.append(f)

        print('*' * 15, 'List Of Files', '*' * 15)
        for i, file in enumerate(only_wave_files):
            print('%d\t->\t%s' % (i, file))

        '''''
        wybór pliku
        '''''

        choice = int(input("\nChoose file: "))
        print('Choosen file: %s' % only_wave_files[choice])
        self.file = os.path.join(DIRECTORY, only_wave_files[choice])
        # print(self.file)
    def get_file(self):
        return self.file

    main_menu = {
        'read_file': choose_file,
        'T60': None,
        'blank': None
    }

def update():
    return {
            1: new_file.file,
            2: new_file.t60,
            3: new_file.colour
            }

new_file = Data

current_task = -1




menu = new_file.main_menu
new_file.main_menu_values = {
    1: new_file.file,
    2: new_file.t60,
    3: new_file.colour
}

values = new_file.main_menu_values

while True:

    # show all  functions
    print('*'*5, 'MENU', '*'*15,'DATA','*'*10)
    for i, option in enumerate(menu.keys()):
        print('{}) {}{}| {}'.format(i+1, option,' '*(15-len(str(option))),  values[i+1]))
        if new_file.file == 'Empty':
            break
    print('*'*42)

    # choose current task
    current_task = int(input(": "))
    if current_task == 0:
        break
    else:
        for i, option in enumerate(menu.keys()):
            if i+1 == current_task:

                menu[option](new_file)  # wywołaj funkcję z menu
                # except TypeError:
                #     print("Ths option is not a function")
    values = update()

