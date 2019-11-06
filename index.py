import wave
from variables import *
from registry import choose_files
import os

import tkinter as tk
from tkinter import filedialog

root = tk.Tk()

canvas1 = tk.Canvas(root, width=300, height=300, bg='white')
canvas1.pack()


def get_path():

    import_file_path = filedialog.askopenfilename()

    return import_file_path

def open_wav():
    browseButton_Excel = tk.Button(text='Choose file', command=get_path, bg='red', fg='white',
                                   font=('helvetica', 12, 'bold'))
    canvas1.create_window(150, 150, window=browseButton_Excel)
    root.mainloop()

class Data:
    file = 'Empty'
    t60 = None
    colour = None


    main_menu = {
        'read_file': open_wav,
        'T60': None,
        'blank': None
    }


new_file = Data


def update():
    return {
            1: new_file.file,
            2: new_file.t60,
            3: new_file.colour
            }


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

                menu[option]()  # wywołaj funkcję z menu
                # except TypeError:
                #     print("Ths option is not a function")
    values = update()

