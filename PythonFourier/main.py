import cmath
import sys
import time
import numpy as np

from scipy.io import wavfile


def get_all_arguments():
    file_path = str(sys.argv[1])
    block_size = int(sys.argv[2])

    algorithm_option = str(sys.argv[3]) if (len(sys.argv) > 3) else None
    if algorithm_option == 'np_fft':
        func = np.fft.fft
    elif algorithm_option == 'dft':
        func = main.dft
    else:
        func = main.fft_vectorized

        if np.log2(block_size) % 1 > 0:
            raise ValueError("Die Groesse des Samples muss eine Potenz von 2 sein, da sonst der Algorihtmus nicht funktioniert.")

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
Außerdem zeigt der Autor, dass seine DFT Implementierung 1000-mal langsamer ist, als die Implementierung von numpy.

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

'''
Der fuer die Aufgabe 01 eigentliche Analyse Algorithmus
'''
def analyze(data, block_size, fourier_function):
    num_samples = len(data)
    num_blocks = num_samples - block_size + 1

    aggregated_fft = np.zeros(block_size//2) #Redundanz der Spiegelung entfernen

    # Fuer jeden Datenblock wird die jeweilige ausgewaehlte Funktion angewendet.
    for i in range(num_blocks):
        block = data[i:i+block_size]
        fft_result = fourier_function(block)

        # Summiere alle Ergebnisse auf
        aggregated_fft += np.abs(fft_result[:block_size//2])

    # Wir berechnen den Mittelwert, da die Summen sonst zu groß sind
    aggregated_fft /= num_blocks

    return aggregated_fft

'''
Die Umrechung zu Dezibel (dB) ist optional.
Ich habe dies nur hinzugefügt, damit die Diagramme auch etwas variieren.
Außerdem sieht man mit der Umwandlung so einige Hauptfrequenzen auf dem Spektrogram besser.
'''
def magnitude_to_dB(fft_result):
    magnitude = np.abs(fft_result)
    return 20 * np.log10(magnitude)

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

    file_path, block_size, fourier_function = get_all_arguments()
    wav_data, sample_rate = analyze_wav_file(file_path)
    aggregated_fft = analyze(wav_data, block_size, fourier_function)

    write_data_to_file([sample_rate, block_size], 'sample_rate_and_block_size.txt')
    write_data_to_file(aggregated_fft, 'aggregated_fft.txt')
    write_data_to_file(magnitude_to_dB(aggregated_fft), 'aggregated_fft_db.txt')

    run_time = time.time() - start_time
    print_run_time(run_time)


if __name__ == "__main__":
    main()

#TODO: Mit den Blockgrößen herumexperimentieren und dokumentieren