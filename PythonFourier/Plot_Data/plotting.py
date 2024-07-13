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

def plot_data_together(data01_x, data01_y, data02_x, data02_y, data03_x, data03_y, yLabel, title):
    plt.figure(figsize=(10, 6))

    plt.plot(data01_x, data01_y, color='blue', marker='.', linestyle='-')
    plt.plot(data02_x, data02_y, color='red', marker='.', linestyle='')
    plt.plot(data03_x, data03_y, color='green', marker='.', linestyle='-')

    plt.xlabel('Frequenz (Hz)')
    plt.ylabel(yLabel)
    plt.title(title)
    plt.grid(True)
    plt.show()

def plot_spectrogram(data, sample_rate, block_size):
    plt.figure(figsize=(10, 6))
    plt.specgram(data, NFFT=int(block_size), Fs=sample_rate)

    plt.xlabel('Zeit (s)')
    plt.ylabel('Frequenz (Hz)')
    plt.title('Spektrogramm')
    plt.colorbar(label='dB')
    plt.ylim(0, sample_rate / 2)
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
    other_data = read_data_as_np_array('sr_bs_t.txt')
    aggregated_fft = read_data_as_np_array('aggregated_fft.txt')
    wav_data = read_data_as_np_array("wav_data.txt")

    sample_rate, block_size, threshold = other_data[0], other_data[1], other_data[2]

    main_frequencies, peaks = get_main_frequencies_with_amplitude(aggregated_fft, sample_rate, block_size)

    # Berechne die Frequenzachse
    frequency_axis = [index * sample_rate / block_size for index in range(len(aggregated_fft))]

    # Plot
    plot_data(frequency_axis, aggregated_fft, 'blue', '-', 'Amplitude', 'Frequenzspektrum')
    plot_data([frequency_axis[peak] for peak in peaks], aggregated_fft[peaks], 'red', '', 'Amplitude', 'Hauptfrequenzen und ihre Amplitude')


    plot_data_together(
        frequency_axis,
        aggregated_fft,
        [frequency_axis[peak] for peak in peaks],
        aggregated_fft[peaks],
        frequency_axis,
        [threshold] * len(frequency_axis),
        'Amplitude',
        'Frequenzspektrum mit Hauptfrequenzen'
    )

    plot_spectrogram(wav_data, sample_rate, block_size)


    for (freq, index) in [(main_frequencies[index], peaks[index]) for index in range(len(main_frequencies))]:
        print("Main Frequency {} with amplitude {} at index {}".format(freq, aggregated_fft[index], index))


if __name__ == "__main__":
    main()