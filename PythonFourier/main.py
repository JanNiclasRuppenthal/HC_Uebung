import cmath
import sys
import time

import numpy as np

from scipy.io import wavfile

# Aufgabe 2
import tracemalloc


def get_all_arguments():
    file_path = str(sys.argv[1])
    block_size = int(sys.argv[2])

    algorithm_option = str(sys.argv[3]) if (len(sys.argv) > 3) else None
    if algorithm_option == 'rec_fft':
        func = fft
    elif algorithm_option == 'vec_fft':
        func = fft_vectorized

        if np.log2(block_size) % 1 > 0:
            raise ValueError("Die Groesse des Samples muss eine Potenz von 2 sein, da sonst der Algorihtmus nicht funktioniert.")

    elif algorithm_option == 'dft':
        func = dft
    elif algorithm_option is None or algorithm_option == "np_fft":
        func = np.fft.fft 

    return file_path, block_size, func


def analyze_wav_file(file_path):
    sample_rate, data = wavfile.read(file_path)

    ''' 
    Falls zwei Kanaele (Stereo) in der WAV-Datei existieren, 
    dann schneiden wir einen Kanal ab, um Rechen- sowie Laufzeit zu sparen.
    '''
    if len(data.shape) > 1:
        data = data[:, 0]

    return data, sample_rate

'''
Diese Methode wurde von ChatGPT generiert.
Ich habe die Methode nicht wirklich getestet, da die DFT sehr viel Rechenzeit benoetigt.
'''
def dft(data_block):
    N = len(data_block)
    X = np.zeros(N, dtype=complex)
    for k in range(N):
        for n in range(N):
            X[k] += data_block[n] * cmath.exp(-2j * np.pi * k * n / N)
    return X


'''
Die FFT Implementierung habe ich von der folgenden Webseite:
https://jakevdp.github.io/blog/2013/08/28/understanding-the-fft/

Die Webseite ist sehr interessant, da sie verschiedene Implementierungen miteinander vergleicht.
Ausserdem zeigt der Autor, dass seine DFT Implementierung 1000-mal langsamer ist, als die Implementierung von numpy.

Ich habe den Code ein wenig angepasst.
'''
def fft_vectorized(data_block):
    data_block = np.asarray(data_block, dtype=float)
    block_size = len(data_block)

    N_min = min(block_size, 32)

    # Berechne DFT auf ein Unterproblem mit einer Groesse von N_min <= 32
    n = np.arange(N_min)
    k = n[:, None]
    M = np.exp(-2j * np.pi * n * k / N_min)
    X = np.dot(M, data_block.reshape((N_min, -1)))

    # Berechne FFT iterativ, anstatt rekursiv
    while X.shape[0] < block_size:
        X_even = X[:, :X.shape[1]//2]
        X_odd = X[:, X.shape[1]//2:]
        factor = np.exp(-1j * np.pi * np.arange(X.shape[0])
                        / X.shape[0])[:, None]
        X = np.vstack([X_even + factor * X_odd,
                       X_even - factor * X_odd])

    return X.ravel()


def fft(x):
    N = len(x)
    if N <= 1:
        return x
    even = fft(x[::2])
    odd = fft(x[1::2])
    factor = np.exp(-2j * np.pi * np.arange(N) / N)
    return np.concatenate([even + factor[:N//2] * odd,
                           even + factor[N//2:] * odd])

'''
Der fuer die Aufgabe 01 eigentliche Analyse Algorithmus
'''
def analyze(data, block_size, fourier_function):
    num_samples = len(data)
    num_blocks = num_samples - block_size + 1

    aggregated_fft = np.zeros(block_size//2) #Redundanz der Spiegelung entfernen

    current, peak = tracemalloc.get_traced_memory()
    currentDataMB = [current/10**6]
    peakDataMB = [peak/10**6]

    # Fuer jeden Datenblock wird die jeweilige ausgewaehlte Funktion angewendet.
    for i in range(num_blocks):
        tracemalloc.reset_peak()
        block = data[i:i+block_size]
        fft_result = fourier_function(block)

        '''
        Summiere alle Ergebnisse auf.
        Wir verwenden den Absolutbetrag der Ergebnisse, da diese komplexe Zahlen sind.
        Der Betrag einer komplexen Zahl ist die Entfernung der Zahl zum Nullpunkt im komplexen Raum.
        '''
        aggregated_fft += np.abs(fft_result[:block_size//2])

        current, peak = tracemalloc.get_traced_memory()
        currentDataMB.append(current/10**6)
        peakDataMB.append(peak/10**6)


    # Wir berechnen den Mittelwert, da die Summen sonst zu gross sind
    aggregated_fft /= num_blocks

    current, peak = tracemalloc.get_traced_memory()
    currentDataMB.append(current/10**6)
    peakDataMB.append(peak/10**6)
    write_data_to_file(currentDataMB, "currentMB.txt")
    write_data_to_file(peakDataMB, "peakMB.txt")

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
    '''
    Die Zeit wird nur als Zusatz gemessen.
    Meines Erachtens sollte man auch neben dem Speicher immer die Zeit betrachten.
    '''
    start_time = time.time()
    tracemalloc.start()

    file_path, block_size, fourier_function = get_all_arguments()
    wav_data, sample_rate = analyze_wav_file(file_path)

    current, peak = tracemalloc.get_traced_memory()
    print(f"Before Fourier Analysis: Memory usage is {current / 10**6}MB; Peak was {peak / 10**6}MB")
    aggregated_fft = analyze(wav_data, block_size, fourier_function)

    current, peak = tracemalloc.get_traced_memory()
    print(f"After Fourier Analysis: Memory usage is {current / 10**6}MB; Peak was {peak / 10**6}MB")
    tracemalloc.stop()

    write_data_to_file([sample_rate, block_size], 'sample_rate_and_block_size.txt')
    write_data_to_file(aggregated_fft, 'aggregated_fft.txt')

    run_time = time.time() - start_time
    print_run_time(run_time)


if __name__ == "__main__":
    main()
