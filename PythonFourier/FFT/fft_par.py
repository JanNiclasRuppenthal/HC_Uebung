import sys
import time

import numpy as np

from scipy.io import wavfile

# Neu fuer Aufgabe 03
import os
import threading

def get_all_arguments():
    file_path = str(sys.argv[1])
    block_size = int(sys.argv[2])

    if block_size < 64:
        block_size = 64
    elif block_size > 512:
        block_size = 512

    shift_size = int(sys.argv[3])
    if shift_size < 1:
        shift_size = 1
    elif shift_size > block_size:
        shift_size = block_size

    threshold = int(sys.argv[4])

    return file_path, block_size, shift_size, threshold


def analyze_wav_file(file_path):
    sample_rate, data = wavfile.read(file_path)

    ''' 
    Falls zwei Kanaele (Stereo) in der WAV-Datei existieren, 
    dann schneiden wir einen Kanal ab, um Rechen- sowie Laufzeit zu sparen.
    '''
    if len(data.shape) > 1:
        data = data[:, 0]

    return data, sample_rate



def fft_thread(id, lock, cpu_count, data, block_size, shift_size):
    global aggregated_fft
    for i in range(id*shift_size, len(data) - block_size + 1, cpu_count * shift_size):
        block = data[i:i+block_size]
        fft_result = np.fft.fft(block)

        '''
        Bei der Addition der Ergebnisse muss man darauf achten, dass man diese Operation synchronisiert, da es zu Fehler
        kommen kann (z.B Race Conditions). Deswegen habe ich einen Lock verwendet, sodass die Threads nacheinander die 
        Ergebniss addiert.
        '''
        lock.acquire()
        aggregated_fft += np.abs(fft_result[:block_size//2])
        lock.release()


def analyze(data, block_size, shift_size):
    '''
    Setze die Variable aggregated_fft global, da sie von allen Threads genutzt werden muss. Damit koennen die Ergebnisse
    zwischengespeichert werden.
    '''
    global aggregated_fft
    num_samples = len(data)
    num_blocks = (num_samples - block_size) // shift_size + 1
    aggregated_fft = np.zeros(block_size//2) #Redundanz der Spiegelung entfernen

    #Neu fuer die Augabe 03:

    #Initialsiere weitere notwendige Variablen fuer die Parallelisierung
    cpu_count = os.cpu_count()
    lock = threading.Lock()
    threads = []

    '''
    Jeder Thread bekommt eine ID, damit man Striping auf den Datenblock verwenden kann.
    '''
    for id in range(cpu_count):
        thread = threading.Thread(target=fft_thread,
                 args=(id, lock, cpu_count, data, block_size, shift_size))
        threads.append(thread)
        thread.start()

    # Warte bis alle Threads ihre Arbeit beendet haben.
    for thread in threads:
        thread.join()

    aggregated_fft = np.array(aggregated_fft) / num_blocks

    return aggregated_fft


'''
Einfache Hilfsfunktion, damit ich die relevanten in einer weiteren Datei weiterverarbeiten kann.
'''
def write_data_to_file(data, file_path):
    with open(file_path, 'w') as file:
        for item in data:
            file.write(str(item) + '\n')


def print_run_time(run_time):
    minutes = run_time // 60
    seconds = run_time % 60

    print('Laufzeit: {} Minuten und {:.2f} Sekunden'.format(minutes, seconds))

def main():
    start_time = time.time()

    file_path, block_size, shift_size, threshold = get_all_arguments()
    wav_data, sample_rate = analyze_wav_file(file_path)

    aggregated_fft = analyze(wav_data, block_size, shift_size)

    run_time = time.time() - start_time
    print_run_time(run_time)

    # Ab hier soll nicht mehr die Zeit gemessen werden, da ich nur die Zeit fuer eine Fourieranalyse haben moechte
    write_data_to_file([sample_rate, block_size, threshold], 'sr_bs_t.txt')
    write_data_to_file(aggregated_fft, 'aggregated_fft.txt')
    write_data_to_file(wav_data, 'wav_data.txt')

    result = [(index * sample_rate / block_size, aggregated_fft[index]) for index in range(len(aggregated_fft)) if aggregated_fft[index] > threshold]

    print(result)


if __name__ == "__main__":
    main()
