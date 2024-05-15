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

def plot_data_together(data01_x, data01_y, data02_x, data02_y, color01, color02, linestyle01, linestyle02, yLabel, title):
    plt.figure(figsize=(10, 6))

    plt.plot(data01_x, data01_y, color=color01, marker='.', linestyle=linestyle01)
    plt.plot(data02_x, data02_y, color=color02, marker='.', linestyle=linestyle02)

    plt.xlabel('Frequenz (Hz)')
    plt.ylabel(yLabel)
    plt.title(title)
    plt.grid(True)
    plt.show()


'''
Finde zuerst allen lokalen Maxima des Spektrogramms durch die Methode find_peaks aus scipy.signal.
Danach werden aus den Indizes die entsprechenden Frequenzen umgerechnet.

Rueckgabe sind die Hauptfrequenzen mit ihren Indizes
'''
def get_main_frequencies_with_amplitude(aggregated_fft, sample_rate, block_size):
    peaks, _ = find_peaks(aggregated_fft)

    main_frequencies = []
    for peakIndex in peaks:
        main_frequencies.append(peakIndex * sample_rate / block_size)

    return main_frequencies, peaks



def main():
    other_data = read_data_as_np_array('sample_rate_and_block_size.txt')
    aggregated_fft = read_data_as_np_array('aggregated_fft.txt')
    aggregated_fft_db = read_data_as_np_array('aggregated_fft_db.txt')

    sample_rate, block_size = other_data[0], other_data[1]

    main_frequencies, peaks = get_main_frequencies_with_amplitude(aggregated_fft, sample_rate, block_size)

    # Berechne die Frequenzachse
    frequency_axis = [index * sample_rate / block_size for index in range(len(aggregated_fft))]

    # Plot des Spektrogramms
    plot_data(frequency_axis, aggregated_fft, 'blue', '-', 'Amplitude', 'Spektrogramm')
    plot_data([frequency_axis[peak] for peak in peaks], aggregated_fft[peaks], 'red', '', 'Amplitude', 'Hauptfrequenzen und ihre Amplitude')

    # Verkleinere das Diagramm
    max_len = frequency_axis.index([frequency_axis[peak] for peak in peaks][-1])

    plot_data_together(
        frequency_axis[:max_len],
        aggregated_fft[:max_len],
        [frequency_axis[peak] for peak in peaks],
        aggregated_fft[peaks],
        'blue',
        'red',
        '-',
        '',
        'Amplitude',
        'Spektrogramm mit Markierung der Hauptfrequenzen'
    )


    for (freq, index) in [(main_frequencies[index], peaks[index]) for index in range(len(main_frequencies))]:
        print("Main Frequency {} with amplitude {} at index {}".format(freq, aggregated_fft[index], index))


if __name__ == "__main__":
    main()