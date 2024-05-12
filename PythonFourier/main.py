import numpy as np
import matplotlib.pyplot as plt
from scipy.io import wavfile
import time

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

def plot_frequency_mean(frequencies, mean_amplitudes):
    plt.figure(figsize=(10, 6))
    plt.plot(frequencies, mean_amplitudes, color='blue', marker='.')
    plt.xlabel('Frequenz (Hz)')
    plt.ylabel('Durchschnitt Amplitude')
    plt.title('Durchschnitt Amplitude pro Frequenz')
    plt.grid(True)
    plt.show()

def plot_frequency_std(frequencies, std_amplitudes):
    plt.figure(figsize=(10, 6))
    plt.plot(frequencies, std_amplitudes, color='orange', marker='.')
    plt.xlabel('Frequenz (Hz)')
    plt.ylabel('Standard Abweichung der Amplitude')
    plt.title('Standard Abweichung der Amplitude pro Frequenz')
    plt.grid(True)
    plt.show()

def plot_main_frequencies(main_frequencies, main_amplitudes):
    plt.figure(figsize=(10, 6))
    plt.scatter(main_frequencies, main_amplitudes, color='red', marker='.')
    plt.xlabel('Frequenz (Hz)')
    plt.ylabel('Amplitude')
    plt.title('Hauptfrequenzen und ihre Amplituden')
    plt.grid(True)
    plt.legend()
    plt.show()

def plot_phase_mean(frequencies, mean_phases):
    plt.figure(figsize=(10, 6))
    plt.plot(frequencies, mean_phases, color='green', marker='.')
    plt.xlabel('Frequenz (Hz)')
    plt.ylabel('Durchschnitt der Phase')
    plt.title('Durchschnitt Phase pro Frequenz')
    plt.grid(True)
    plt.show()

def plot_phase_std(frequencies, std_phases):
    plt.figure(figsize=(10, 6))
    plt.plot(frequencies, std_phases, color='purple', marker='.')
    plt.xlabel('Frequenz (Hz)')
    plt.ylabel('Standard Abweichung der Phase')
    plt.title('Standard Abweichung der Phase pro Frequenz')
    plt.grid(True)
    plt.show()

def plot_spectrogram(sample_rate, frequencies, amplitudes):
    plt.figure(figsize=(10, 6))
    plt.plot(frequencies, amplitudes, color='blue')
    plt.xlabel('Frequenz (Hz)')
    plt.ylabel('Amplitude')
    plt.title('Spektrogramm')
    plt.grid(True)
    plt.show()

if __name__ == "__main__":

    startTime = time.time()

    file_path = "../resources/Geheimnisvolle_Wellenlaengen.wav"
    block_size = 512
    # Sie können die Blockgröße anpassen
    frequencies, mean_amplitudes, std_amplitudes, mean_phases, std_phases, sample_rate, aggregated_fft = analyze_wav_file(file_path, block_size)
    plot_frequency_mean(frequencies, mean_amplitudes)
    plot_frequency_std(frequencies, std_amplitudes)
    plot_main_frequencies(frequencies, mean_amplitudes)
    plot_phase_mean(frequencies, mean_phases)
    plot_phase_std(frequencies, std_phases)

    frequency_axis = np.fft.fftfreq(len(aggregated_fft)*2, 1/sample_rate)[:len(aggregated_fft)]
    plot_spectrogram(sample_rate, frequency_axis, aggregated_fft)


    runTime = time.time() - startTime

    minutes = runTime // 60
    seconds = runTime % 60

    print('Laufzeit: {} Minuten und {:.2f} Sekunden'.format(minutes, seconds))

#TODO: Das plotten in eine andere Datei verlagern
#TODO: Eigene fft Methode implementieren
#TODO: Mit den Blockgrößen herumexperimentieren