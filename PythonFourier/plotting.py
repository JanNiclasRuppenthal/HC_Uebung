import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import find_peaks

def read_data_as_np_array(filename):
    return np.loadtxt(filename)

def plot_data(data01, data02, color, linestyle, yLabel, title):
    plt.figure(figsize=(10, 6))
    plt.plot(data01, data02, color=color, marker='.', linestyle=linestyle)
    plt.xlabel('Frequenz (Hz)')
    plt.ylabel(yLabel)
    plt.title(title)
    plt.grid(True)
    plt.show()

def main():
    sample_rate = read_data_as_np_array('sample_rate.txt')
    aggregated_fft = read_data_as_np_array('aggregated_fft.txt')


    # Berechne die Frequenzachse
    frequency_axis = [index * sample_rate / 1024 for index in range(len(aggregated_fft))]

    # Plot des Spektrogramms
    plot_data(frequency_axis, aggregated_fft, 'blue', '-', 'Amplitude', 'Spektrogramm')

    # Finde die lokalen Maxima in den Amplituden
    peaks, _ = find_peaks(aggregated_fft)

    plot_data([frequency_axis[peak] for peak in peaks], aggregated_fft[peaks], 'red', '', 'Amplitude', 'Hauptfrequenzen und ihre Amplitude')
    plt.show()


    # Ausgabe der Positionen der lokalen Maxima
    print("Positionen der lokalen Maxima:", peaks)
    print("Frequenzen der lokalen Maxima:", [frequency_axis[peak] for peak in peaks])


if __name__ == "__main__":
    main()