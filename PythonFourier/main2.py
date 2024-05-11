import numpy as np
import matplotlib.pyplot as plt
from scipy.io import wavfile

def aggregate_fft(file_path, block_size):
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
    aggregated_fft = np.zeros(block_size//2)

    # Analyse der WAV-Datei in Blöcken
    for i in range(num_blocks):
        # Extrahiere den aktuellen Block
        block = data[i:i+block_size]

        # Berechne die FFT des Blocks
        fft_result = np.fft.fft(block)

        # Zuschneiden der FFT-Ergebnisse auf die gleiche Länge wie aggregated_fft
        fft_result = fft_result[:block_size//2]

        # Addiere die Amplituden der FFT-Ergebnisse
        aggregated_fft += np.abs(fft_result)

    # Mittelwert der aggregierten FFT berechnen
    aggregated_fft /= num_blocks

    return sample_rate, aggregated_fft

def plot_spectrogram(sample_rate, frequencies, amplitudes):
    plt.figure(figsize=(10, 6))
    plt.plot(frequencies, amplitudes)
    plt.xlabel('Frequency (Hz)')
    plt.ylabel('Amplitude')
    plt.title('Spectrogram')
    plt.grid(True)
    plt.show()

if __name__ == "__main__":
    file_path = "../resources/Geheimnisvolle_Wellenlaengen.wav"
    block_size = 1024  # Sie können die Blockgröße anpassen
    sample_rate, aggregated_fft = aggregate_fft(file_path, block_size)
    frequency_axis = np.fft.fftfreq(len(aggregated_fft)*2, 1/sample_rate)[:len(aggregated_fft)]
    plot_spectrogram(sample_rate, frequency_axis, aggregated_fft)
