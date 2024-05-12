import numpy as np
from scipy.io import wavfile
import matplotlib.pyplot as plt

def analyze_wav_file(file_path, block_size, overlap):
    # WAV-Datei einlesen
    sample_rate, data = wavfile.read(file_path)

    # Überprüfen, ob die WAV-Datei Stereo ist
    if len(data.shape) > 1:
        # Extrahiere nur einen Kanal (nehmen wir den ersten)
        data = data[:, 0]

    # Anzahl der Samples in der WAV-Datei
    num_samples = len(data)

    # Berechne die Anzahl der Blöcke
    num_blocks = (num_samples - block_size) // overlap + 1

    # Liste zur Speicherung der aggregierten FFT-Ergebnisse
    spectrogram = []

    # Analyse der WAV-Datei in Blöcken
    for i in range(num_blocks):
        # Extrahiere den aktuellen Block
        start = i * overlap
        end = start + block_size
        block = data[start:end]

        # Berechne die FFT des Blocks
        fft_result = np.fft.fft(block, n=block_size)

        # Speichere die Amplituden der FFT-Ergebnisse
        amplitude_spectrum = np.abs(fft_result)[:block_size // 2 + 1]

        # Konvertiere die Amplituden in Dezibel (dB)
        amplitude_spectrum_db = 20 * np.log10(amplitude_spectrum)

        # Füge das Amplitudenspektrum zum Spektrogramm hinzu
        spectrogram.append(amplitude_spectrum_db)

    # Konvertiere das Spektrogramm in ein Numpy-Array
    spectrogram = np.array(spectrogram)

    # Frequenzachse erstellen
    frequency_axis = np.fft.fftfreq(block_size, 1 / sample_rate)[:block_size // 2 + 1]

    return frequency_axis, spectrogram, sample_rate

def plot_spectrogram(frequencies, spectrogram, sample_rate):
    plt.figure(figsize=(10, 6))
    plt.imshow(spectrogram.T, aspect='auto', origin='lower', extent=(0, len(spectrogram) / sample_rate, frequencies[0], frequencies[-1]), cmap='viridis')
    plt.colorbar(label='Amplitude (dB)')
    plt.xlabel('Time (s)')
    plt.ylabel('Frequency (Hz)')
    plt.title('Spectrogram')
    plt.show()

if __name__ == "__main__":
    file_path = "../resources/Geheimnisvolle_Wellenlaengen.wav"
    block_size = 512
    overlap = 1
    frequencies, spectrogram, sample_rate = analyze_wav_file(file_path, block_size, overlap)
    plot_spectrogram(frequencies, spectrogram, sample_rate)
