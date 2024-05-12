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

def scatter_data(data01, data02, color, yLabel, title):
    plt.figure(figsize=(10, 6))
    plt.scatter(data01, data02, color=color)
    plt.xlabel('Frequenz (Hz)')
    plt.ylabel(yLabel)
    plt.title(title)
    plt.grid(True)
    plt.show()

def main():

    frequencies = read_data_as_np_array('frequencies.txt')
    mean_amplitudes = read_data_as_np_array('mean_amplitudes.txt')
    std_amplitudes = read_data_as_np_array('std_amplitudes.txt')
    mean_phases = read_data_as_np_array('mean_phases.txt')
    std_phases = read_data_as_np_array('std_phases.txt')
    sample_rate = read_data_as_np_array('sample_rate.txt')
    aggregated_fft = read_data_as_np_array('aggregated_fft.txt')



    plot_data(frequencies, mean_amplitudes, 'blue', '-', 'Durchschnittliche Amplitude', 'Durchschnittliche Amplitude pro Frequenz')
    plot_data(frequencies, std_amplitudes, 'orange', '-', 'Standard Abweichung der Amplitude', 'Standard Abweichung der Amplitude pro Frequenz')

    scatter_data(frequencies, mean_amplitudes, 'red', 'Amplitude', 'Hauptfrequenzen und ihre Amplituden')

    plot_data(frequencies, mean_phases, 'green', '-', 'Durchschnittliche Phase', 'Durchschnittliche Phase pro Frequenz')
    plot_data(frequencies, std_phases, 'purple', '-', 'Standard Abweichung der Phase', 'Standard Abweichung der Phase pro Frequenz')


    # Berechne die Frequenzachse
    frequency_axis = np.fft.fftfreq(len(aggregated_fft)*2, 1/sample_rate)[:len(aggregated_fft)]

    # Plot des Spektrogramms
    plot_data(frequency_axis, aggregated_fft, 'blue', '-', 'Amplitude', 'Spektrogramm')

    # Finde die lokalen Maxima in den Amplituden
    peaks, _ = find_peaks(aggregated_fft)

    plot_data(frequency_axis[peaks], aggregated_fft[peaks], 'red', '', 'Amplitude', 'Hauptfrequenzen und ihre Amplitude')
    plt.show()


    # Ausgabe der Positionen der lokalen Maxima
    print("Positionen der lokalen Maxima:", peaks)
    print("Frequenzen der lokalen Maxima:", frequency_axis[peaks])


if __name__ == "__main__":
    main()