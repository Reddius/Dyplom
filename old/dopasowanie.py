from old.read_chunks import *

def detect_silence(sound: any, silence_threshold: float = -30.0, chunk_size: int = 10) -> str:
    '''
    sound is a pydub.AudioSegment
    silence_threshold in dB
    chunk_size in ms

    iterate over chunks until you find the first one with sound
    '''
    trim_ms = 0 # ms

    assert chunk_size > 0, "chunk cant be smaller than 0" # to avoid infinite loop
    while sound[trim_ms:trim_ms+chunk_size].dBFS < silence_threshold and trim_ms < len(sound):
        trim_ms += chunk_size

    return trim_ms


def get_peaks(sound: any, chunk_size: int = 1) -> list:
    """
zapisuje peaki dBFS w chunkach rozmiaru 1ms
służy do dopasowania dwóch plików wav ze sobą w czasie
    :param sound:  sound = AudioSegment.from_file(path_to_audio_file, format="wav")
    :param chunk_size: najlepiej 1ms
    :return:
    """
    assert chunk_size > 0, "chunk size for detect delta should be >0"
    peaks = []
    for i, chunk in enumerate(sound[::chunk_size]):
        peaks.append([i, chunk.dBFS])

    return peaks


def silences(path_to_audio_file):
    """
funkcja zwraca w ms początek nagrania i koniec nagrania + połączone oba czasy
    :param path_to_audio_file:
    :return:
    """
    sound = AudioSegment.from_file(path_to_audio_file, format="wav")

    # print(sound)
    start_trim = detect_silence(sound)
    end_trim = detect_silence(sound.reverse())

    if start_trim != 0 and end_trim != 0:
        duration = len(sound)
        trimmed_sound = sound[start_trim:duration - end_trim]
        peaks = get_peaks(trimmed_sound)
        new_file = ""
        for letter in path_to_audio_file:
            if letter == ".":
                break
            new_file = new_file + letter
        new_file = new_file + "_trimmed.wav"
        trimmed_sound.export(new_file, format="wav")
        print("created new trimmed file: " + new_file)
    else:
        peaks = get_peaks(sound)
        new_file = path_to_audio_file
        print("no need to trim")

    return start_trim, end_trim, new_file, peaks


def resize(path_to_audio_file, ms):

    sound = AudioSegment.from_file(path_to_audio_file, format="wav")
    silence = AudioSegment.silent(duration=ms)
    sound = silence + sound

    new_file = ""
    for letter in path_to_audio_file:
        if letter == ".":
            break
        new_file = new_file + letter
    new_file = new_file + "_matched.wav"
    sound.export(new_file, format="wav")
    print("created new trimmed file: " + new_file)
    return new_file

def get_delay(peaks: list, peaks2: list) -> [int,int]:
    """
wylicza opróźnienie jednego pliku względem drugiego na podstawie poziomu dźwięku w
poszczególnych chunkach [peaks i peaks2] domyslnie długość chunka =1ms

    :param peaks: lista poziomów dźwięku w chunkach
    :param peaks2: -||-
    :return: opóźnienie w ms
    """
    average = 100
    ms = 0
    file = 0
    MAX_DELAY = 100 #ms

    for delay in range(MAX_DELAY):
        delta = []
        for i in range(min(len(peaks) - MAX_DELAY, len(peaks2) - MAX_DELAY)):
            delta.append(abs(peaks[i + delay][1] - peaks2[i][1]))
        if sum(delta) / len(delta) < average:
            average = sum(delta) / len(delta)
            ms = delay
        if average < 0.5:
            break

    if average > 0.5:
        file = 1
        ms = 0

        for delay in range(MAX_DELAY):
            delta = []
            for i in range(min(len(peaks) - MAX_DELAY, len(peaks2) - MAX_DELAY)):
                delta.append(abs(peaks2[i + delay][1] - peaks[i][1]))
            if sum(delta) / len(delta) < average:
                average = sum(delta) / len(delta)
                ms = delay
            if average < 0.5:
                break
    return ms, file

def match(wavefiles, choice):
    """
Dopasowanie plików:
Krok 1: Ucinanie ciszy na początku pliku
Krok 2: Dopasowanie ewentualego przesunięcia w czasie pomiędzy sygnałami

    :param wavefiles: lista objektów klasy
    :param choice: lista wybranych plików z input()
    :return:
    """
    start, end, f1_new, peaks = silences(choice[0])
    start2, end2, f2_new, peaks2 = silences(choice[1])

    if f1_new != choice[0]:
        wavefiles.append(File(f1_new, "File 1 trimmed"))

    if f2_new != choice[1]:
        wavefiles.append(File(f2_new, "File 2 trimmed"))

    # get delay
    # which daje info o tym który plk jest opóźniony

    ms, which = get_delay(peaks, peaks2)

    print("Delay between files: %dms" % ms)

    if which == 1 and ms != 0:
        resized_file = resize(f1_new, ms)
        wavefiles.append(File(resized_file, "File 1 resized"))
        print('File 1 resized to match file 2')
    elif which == 0 and ms != 0:
        resized_file = resize(f2_new, ms)
        wavefiles.append(File(resized_file, "File 2 resized"))
        print('File 2 resized to match file 1')
    else:
        print("no need to resize")

    return wavefiles
