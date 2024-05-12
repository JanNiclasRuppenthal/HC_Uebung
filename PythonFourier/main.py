import numpy as np
from scipy.io import wavfile
import time

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
    aggregated_fft = np.zeros(block_size) #//2) Redundanz der Spiegelung entfernen?

    # Liste zur Speicherung der Frequenzanteile
    frequencies = []
    amplitudes = []
    phases = []

    # Analyse der WAV-Datei in Blöcken
    for i in range(num_blocks):
        # Extrahiere den aktuellen Block
        block = data[i:i+block_size]

        # Berechne die FFT des Blocks
        fft_result = np.fft.fft(block)
        # fft_result = FFT_vectorized(block)

        # Finde die Frequenz mit der höchsten Amplitude
        max_freq_index = np.argmax(np.abs(fft_result))
        max_freq = max_freq_index * sample_rate / block_size

        # Finde die Amplitude dieser Frequenz
        amplitude = np.abs(fft_result[max_freq_index])

        # Finde die Phase dieser Frequenz
        phase = np.angle(fft_result[max_freq_index])

        # Addiere die Amplituden der FFT-Ergebnisse
        aggregated_fft += np.abs(fft_result)

        frequencies.append(max_freq)
        amplitudes.append(amplitude)
        phases.append(phase)

    # Mittelwert der aggregierten FFT berechnen
    aggregated_fft /= num_blocks

    # Aggregiere die Ergebnisse pro Frequenz
    unique_frequencies = np.unique(frequencies)
    mean_amplitudes = []
    std_amplitudes = []
    mean_phases = []
    std_phases = []

    for freq in unique_frequencies:
        freq_indices = [i for i, f in enumerate(frequencies) if f == freq]
        freq_amplitudes = [amplitudes[i] for i in freq_indices]
        freq_phases = [phases[i] for i in freq_indices]

        mean_amplitude = np.mean(freq_amplitudes)
        std_amplitude = np.std(freq_amplitudes)
        mean_phase = np.mean(freq_phases)
        std_phase = np.std(freq_phases)

        mean_amplitudes.append(mean_amplitude)
        std_amplitudes.append(std_amplitude)
        mean_phases.append(mean_phase)
        std_phases.append(std_phase)

    return unique_frequencies, mean_amplitudes, std_amplitudes, mean_phases, std_phases, sample_rate, aggregated_fft

def write_data_to_file(data, file_path):
    with open(file_path, 'w') as file:
        for item in data:
            file.write(str(item) + '\n')

if __name__ == "__main__":

    startTime = time.time()

    file_path = "../resources/Geheimnisvolle_Wellenlaengen.wav"  #sys.argv[1]
    block_size = 512 #sys.argv[2]
    # Sie können die Blockgröße anpassen
    frequencies, mean_amplitudes, std_amplitudes, mean_phases, std_phases, sample_rate, aggregated_fft = analyze_wav_file(file_path, block_size)

    write_data_to_file(frequencies, 'frequencies.txt')
    write_data_to_file(mean_amplitudes, 'mean_amplitudes.txt')
    write_data_to_file(std_amplitudes, 'std_amplitudes.txt')
    write_data_to_file(mean_phases, 'mean_phases.txt')
    write_data_to_file(std_phases, 'std_phases.txt')
    write_data_to_file([sample_rate], 'sample_rate.txt')
    write_data_to_file(aggregated_fft, 'aggregated_fft.txt')

    runTime = time.time() - startTime

    minutes = runTime // 60
    seconds = runTime % 60

    print('Laufzeit: {} Minuten und {:.2f} Sekunden'.format(minutes, seconds))

#TODO: Block_size halbieren?
#TODO: Mit den Blockgrößen herumexperimentieren