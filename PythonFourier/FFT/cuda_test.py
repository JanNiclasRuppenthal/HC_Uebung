import numpy as np
import scipy.io.wavfile as wavfile
from numba import cuda, float32
import math
import matplotlib.pyplot as plt

# Funktion zum Lesen der WAV-Datei
def read_wav(file_path):
    sample_rate, data = wavfile.read(file_path)
    if data.ndim == 2:  # falls Stereo, nur einen Kanal nehmen
        data = data[:, 0]
    return sample_rate, data

# CUDA-Kernel für FFT
@cuda.jit
def sliding_fft(input_signal, window_size, step_size, output_fft):
    idx = cuda.grid(1)
    if idx * step_size + window_size < input_signal.size:
        # Fenster anwenden
        windowed_signal = input_signal[idx * step_size: idx * step_size + window_size]
        fft_result = cuda.local.array(shape=(window_size,), dtype=float32)

        # FFT durchführen (Cooley-Tukey-Algorithmus für Einfachheit)
        N = window_size
        for k in range(N):
            real_sum = 0.0
            imag_sum = 0.0
            for n in range(N):
                angle = 2.0 * math.pi * k * n / N
                real_sum += windowed_signal[n] * math.cos(angle)
                imag_sum -= windowed_signal[n] * math.sin(angle)
            fft_result[k] = math.sqrt(real_sum**2 + imag_sum**2)

        for k in range(window_size):
            output_fft[idx, k] = fft_result[k]

def plot_spectrum(output_fft, sample_rate, window_size, step_size):
    time_bins, freq_bins = output_fft.shape
    t = np.arange(0, time_bins * step_size / sample_rate, step_size / sample_rate)
    f = np.linspace(0, sample_rate / 2, window_size // 2)

    plt.figure(figsize=(12, 6))
    plt.pcolormesh(t, f, output_fft[:, :window_size // 2].T, shading='gouraud')
    plt.title('Spektrogramm')
    plt.xlabel('Zeit [s]')
    plt.ylabel('Frequenz [Hz]')
    plt.colorbar(label='Amplitude')
    plt.show()

def plot_frequency_spectrum(aggregated_dft, sample_rate, block_size):
    freqs = np.fft.fftfreq(block_size, d=1/sample_rate)[:block_size//2]
    plt.figure(figsize=(10, 6))
    plt.plot(freqs, aggregated_dft)
    plt.xlabel('Frequenz (Hz)')
    plt.ylabel('Amplitude')
    plt.title('Frequenzspektrum')
    plt.grid(True)
    plt.show()

def main():
    # Parameter
    file_path = 'your_audio_file.wav'  # Pfad zu Ihrer WAV-Datei
    window_size = 1024
    step_size = 512

    # WAV-Datei lesen
    sample_rate, data = read_wav(file_path)

    # Anzahl der Fenster bestimmen
    num_windows = (len(data) - window_size) // step_size + 1

    # Ausgabe-Array zuweisen
    output_fft = np.zeros((num_windows, window_size), dtype=np.float32)

    # Daten auf das Gerät verschieben
    d_input_signal = cuda.to_device(data.astype(np.float32))
    d_output_fft = cuda.to_device(output_fft)

    # Blöcke konfigurieren
    threads_per_block = 128
    blocks_per_grid = (num_windows + (threads_per_block - 1)) // threads_per_block

    # Kernel starten
    sliding_fft[blocks_per_grid, threads_per_block](d_input_signal, window_size, step_size, d_output_fft)

    # Ergebnis zurück auf den Host kopieren
    output_fft = d_output_fft.copy_to_host()

    print("Sliding FFT Ergebnisform:", output_fft.shape)

    # Frequenzspektrum plotten (Spektrogramm)
    plot_spectrum(output_fft, sample_rate, window_size, step_size)

    # Aggregiertes Frequenzspektrum berechnen
    aggregated_dft = np.mean(output_fft, axis=0)[:window_size // 2]

    # Frequenzspektrum plotten (aggregiert)
    plot_frequency_spectrum(aggregated_dft, sample_rate, window_size)

if __name__ == "__main__":
    main()
