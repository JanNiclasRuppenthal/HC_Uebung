import numpy as np
import matplotlib.pyplot as plt
from scipy.io import wavfile

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

        # Finde die Frequenz mit der höchsten Amplitude
        max_freq_index = np.argmax(np.abs(fft_result))
        max_freq = max_freq_index * sample_rate / block_size

        # Finde die Amplitude dieser Frequenz
        amplitude = np.abs(fft_result[max_freq_index])

        # Finde die Phase dieser Frequenz
        phase = np.angle(fft_result[max_freq_index])

        frequencies.append(max_freq)
        amplitudes.append(amplitude)
        phases.append(phase)

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

    return unique_frequencies, mean_amplitudes, std_amplitudes, mean_phases, std_phases

def plot_frequency_mean(frequencies, mean_amplitudes):
    plt.figure(figsize=(10, 6))
    plt.plot(frequencies, mean_amplitudes, marker='o')
    plt.xlabel('Frequency (Hz)')
    plt.ylabel('Mean Amplitude')
    plt.title('Mean Amplitude per Frequency')
    plt.grid(True)
    plt.show()

def plot_frequency_std(frequencies, std_amplitudes):
    plt.figure(figsize=(10, 6))
    plt.plot(frequencies, std_amplitudes, marker='o', color='orange')
    plt.xlabel('Frequency (Hz)')
    plt.ylabel('Standard Deviation of Amplitude')
    plt.title('Standard Deviation of Amplitude per Frequency')
    plt.grid(True)
    plt.show()

def plot_main_frequencies(main_frequencies, main_amplitudes):
    plt.figure(figsize=(10, 6))
    plt.scatter(main_frequencies, main_amplitudes, color='red', label='Main Frequencies')
    plt.xlabel('Frequency (Hz)')
    plt.ylabel('Amplitude')
    plt.title('Main Frequencies and their Amplitudes')
    plt.grid(True)
    plt.legend()
    plt.show()

def plot_phase_mean(frequencies, mean_phases):
    plt.figure(figsize=(10, 6))
    plt.plot(frequencies, mean_phases, marker='o', color='green')
    plt.xlabel('Frequency (Hz)')
    plt.ylabel('Mean Phase')
    plt.title('Mean Phase per Frequency')
    plt.grid(True)
    plt.show()

def plot_phase_std(frequencies, std_phases):
    plt.figure(figsize=(10, 6))
    plt.plot(frequencies, std_phases, marker='o', color='purple')
    plt.xlabel('Frequency (Hz)')
    plt.ylabel('Standard Deviation of Phase')
    plt.title('Standard Deviation of Phase per Frequency')
    plt.grid(True)
    plt.show()

def plot_spectrum(frequencies, amplitudes, sample_rate):
    plt.figure(figsize=(10, 6))
    plt.plot(frequencies, amplitudes)
    plt.xlabel('Frequency (Hz)')
    plt.ylabel('Amplitude')
    plt.title('Frequency Spectrum')
    plt.xlim(0, sample_rate / 2)
    plt.grid(True)
    plt.show()

if __name__ == "__main__":
    file_path = "../resources/Geheimnisvolle_Wellenlaengen.wav"
    block_size = 1024  # Sie können die Blockgröße anpassen
    frequencies, mean_amplitudes, std_amplitudes, mean_phases, std_phases = analyze_wav_file(file_path, block_size)
    plot_frequency_mean(frequencies, mean_amplitudes)
    plot_frequency_std(frequencies, std_amplitudes)
    plot_main_frequencies(frequencies, mean_amplitudes)
    plot_phase_mean(frequencies, mean_phases)
    plot_phase_std(frequencies, std_phases)

    # Zusätzliches Spektraldiagramm
    # sample_rate, data = wavfile.read(file_path)
    # fft_result = np.fft.fft(data)
    # frequency_axis = np.fft.fftfreq(len(fft_result), 1/sample_rate)
    # plot_spectrum(frequency_axis[:len(frequency_axis)//2], np.abs(fft_result)[:len(fft_result)//2], sample_rate)



#TODO: Diagramm in main2.py auch hier reinschreiben
#TODO: Das plotten in eine andere Datei verlagern
#TODO: Mit den Blockgrößen herumexperimentieren