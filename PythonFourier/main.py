import numpy as np
import scipy.io.wavfile as wavfile

def fft_analysis(signal, block_size):
    # Funktion zur Berechnung der diskreten Fourier-Transformation (DFT) eines Signals
    N = len(signal)
    num_blocks = (N - block_size) // block_size + 1
    fft_result = []
    for k in range(num_blocks):
        start = k * block_size
        end = min(start + block_size, N)
        block = signal[start:end]  # Block extrahieren
        if len(block) < block_size:  # Zero-padding für Blöcke, die kürzer als block_size sind
            block = np.append(block, np.zeros(block_size - len(block)))
        fft_block = np.fft.fft(block)  # DFT des Blocks berechnen
        fft_result.append(fft_block)
    return np.array(fft_result)

def main():
    # Pfad zur WAV-Datei
    wav_file = "../resources/Geheimnisvolle_Wellenlaengen.wav"

    # Blockgröße und Verschiebung (Anzahl der Samples)
    block_size = int(input("Geben Sie die Blockgröße in Samples ein: "))

    # WAV-Datei lesen
    sample_rate, data = wavfile.read(wav_file)

    # Wenn die WAV-Datei mehrere Kanäle hat, wählen Sie nur einen Kanal aus (z. B. den linken)
    if len(data.shape) > 1:
        data = data[:, 0]

    # DFT-Analyse durchführen
    dft_result = fft_analysis(data, block_size)

    # Aggregieren der Ergebnisse pro Block
    mean_values = np.mean(dft_result, axis=0)  # Mittelwerte pro Frequenz
    std_values = np.std(dft_result, axis=0)    # Standardabweichungen pro Frequenz

    # Ausgabe der aggregierten Ergebnisse
    print("Aggregierte Ergebnisse pro Frequenz:")
    for i in range(len(mean_values)):
        print("Frequenz {}: Mittelwert = {:.2f}, Standardabweichung = {:.2f}".format(i, mean_values[i], std_values[i]))

    # Phasenwerte für die Berechnung des Mittelwerts und der Standardabweichung
    phase_values = np.angle(dft_result)  # Phasenwerte aus den DFT-Ergebnissen extrahieren

    # Berechnung des Mittelwerts und der Standardabweichung für die Phase
    phase_mean = np.mean(phase_values, axis=0)  # Mittelwert pro Phase
    phase_std_deviation = np.std(phase_values, axis=0)    # Standardabweichung pro Phase

    # Ausgabe der aggregierten Ergebnisse pro Phase
    print("Aggregierte Ergebnisse pro Phase:")
    for i in range(len(phase_mean)):
        print("Phase {}: Mittelwert = {:.2f}, Standardabweichung = {:.2f}".format(i, phase_mean[i], phase_std_deviation[i]))

if __name__ == "__main__":
    main()
