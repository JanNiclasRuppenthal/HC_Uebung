import numpy as np
from scipy.io import wavfile
from scipy.signal import find_peaks
import time
import sys

# You're too slow!
def my_dft(x):
    """Compute the discrete Fourier Transform of the 1D array x"""
    x = np.asarray(x, dtype=float)
    N = x.shape[0]
    n = np.arange(N)
    k = n.reshape((N, 1))
    M = np.exp(-2j * np.pi * k * n / N)
    return np.dot(M, x)



def FFT_vectorized(x):
    """A vectorized, non-recursive version of the Cooley-Tukey FFT"""
    x = np.asarray(x, dtype=float)
    N = x.shape[0]

    if np.log2(N) % 1 > 0:
        raise ValueError("size of x must be a power of 2")

    # N_min here is equivalent to the stopping condition above,
    # and should be a power of 2
    N_min = min(N, 32)

    # Perform an O[N^2] DFT on all length-N_min sub-problems at once
    n = np.arange(N_min)
    k = n[:, None]
    M = np.exp(-2j * np.pi * n * k / N_min)
    X = np.dot(M, x.reshape((N_min, -1)))

    # build-up each level of the recursive calculation all at once
    while X.shape[0] < N:
        X_even = X[:, :X.shape[1]//2]
        X_odd = X[:, X.shape[1]//2:]
        factor = np.exp(-1j * np.pi * np.arange(X.shape[0])
                        / X.shape[0])[:, None]
        X = np.vstack([X_even + factor * X_odd,
                       X_even - factor * X_odd])

    return X.ravel()




def analyze_wav_file(file_path, block_size):
    # WAV-Datei einlesen
    sample_rate, data = wavfile.read(file_path)

    # Überprüfen, ob die WAV-Datei Stereo ist
    if len(data.shape) > 1:
        # Extrahiere nur einen Kanal (nehmen wir den ersten)
        data = data[:, 0]

    # Anzahl der Samples in der WAV-Datei
    num_samples = len(data)

    # Berechne die Anzahl der Blöcke
    num_blocks = num_samples - block_size + 1

    # Liste zur Speicherung der aggregierten FFT-Ergebnisse
    aggregated_fft = np.zeros(block_size//2) #Redundanz der Spiegelung entfernen

    # Analyse der WAV-Datei in Blöcken
    for i in range(num_blocks):
        # Extrahiere den aktuellen Block
        block = data[i:i+block_size]

        # Berechne die FFT des Blocks
        fft_result = np.fft.fft(block)
        # fft_result = my_dft(block)
        # fft_result = FFT_vectorized(block)

        # Addiere die Amplituden der FFT-Ergebnisse
        aggregated_fft += np.abs(fft_result[:block_size//2])

    # Mittelwert der aggregierten FFT berechnen
    aggregated_fft /= num_blocks

    return sample_rate, aggregated_fft


def get_main_frequencies_with_amplitude(aggregated_fft, sample_rate, block_size):
    peaks, _ = find_peaks(aggregated_fft)

    main_frequencies = []
    for peakIndex in peaks:
        main_frequencies.append(peakIndex * sample_rate / block_size)

    return main_frequencies, peaks




def write_data_to_file(data, file_path):
    with open(file_path, 'w') as file:
        for item in data:
            file.write(str(item) + '\n')


if __name__ == "__main__":
    startTime = time.time()

    file_path = sys.argv[1]
    block_size = int(sys.argv[2])

    sample_rate, aggregated_fft = analyze_wav_file(file_path, block_size)

    main_frequencies, peaks = get_main_frequencies_with_amplitude(aggregated_fft, sample_rate, block_size)

    for (freq, index) in [(main_frequencies[index], peaks[index]) for index in range(len(main_frequencies))]:
        print("Main Frequency {} at index {}".format(freq, index))



    write_data_to_file([sample_rate], 'sample_rate.txt')
    write_data_to_file(aggregated_fft, 'aggregated_fft.txt')

    runTime = time.time() - startTime

    minutes = runTime // 60
    seconds = runTime % 60

    print('Laufzeit: {} Minuten und {:.2f} Sekunden'.format(minutes, seconds))

#TODO: Mit den Blockgrößen herumexperimentieren
#TODO: Angabe der Amplituden in dB
#TODO: Kommentare aendern