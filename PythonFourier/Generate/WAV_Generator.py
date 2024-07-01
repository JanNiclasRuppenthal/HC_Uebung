import sys
import numpy as np
from scipy.io.wavfile import write

global duration, sample_rate, timestamps


def sine_wave(frequency):
    return 0.5 * np.sin(2 * np.pi * frequency * timestamps)


def polyphonic_wave(frequencies):
    signal = np.zeros_like(timestamps)
    for frequency in frequencies:
        signal += 0.5 * np.sin(2 * np.pi * frequency * timestamps)
    return signal


def chirp_wave(start_freq, end_freq):
    return 0.5 * np.sin(2 * np.pi * (start_freq + (end_freq - start_freq) * timestamps / duration) * timestamps)


def noise():
    return 0.5 * np.random.normal(0, 1, int(sample_rate * duration))


def am_wave(carrier_freq, mod_freq):
    carrier = np.sin(2 * np.pi * carrier_freq * timestamps)
    modulator = 1 + 0.5 * np.sin(2 * np.pi * mod_freq * timestamps)
    return 0.5 * carrier * modulator


def fm_wave(carrier_freq, mod_freq, mod_index):
    return 0.5 * np.sin(2 * np.pi * carrier_freq * timestamps + mod_index * np.sin(2 * np.pi * mod_freq * timestamps))


def segmented_sine_wave(frequencies, segment_duration):
    signal = np.array([])
    for frequency in frequencies:
        timestamps = np.linspace(0, segment_duration, int(sample_rate * segment_duration), endpoint=False)
        segment = 0.5 * np.sin(2 * np.pi * frequency * timestamps)
        signal = np.concatenate((signal, segment))
    return signal


def sine_wave_with_envelope(frequency):
    envelope = np.linspace(0, 1, int(sample_rate * duration))
    sine_wave = 0.5 * np.sin(2 * np.pi * frequency * timestamps)
    return sine_wave * envelope


def additive_synthesis_wave(fundamental_freq, num_harmonics):
    signal = np.zeros_like(timestamps)
    for i in range(1, num_harmonics + 1):
        signal += (0.5 / i) * np.sin(2 * np.pi * fundamental_freq * i * timestamps)
    return signal


def triangle_wave(frequency):
    period = 1 / frequency
    t_normalized = (timestamps % period) / period
    return 0.5 * (2 * np.abs(2 * t_normalized - 1) - 1)


def square_wave(frequency):
    return 0.5 * np.sign(np.sin(2 * np.pi * frequency * timestamps))


def get_all_arguments():
    filename = str(sys.argv[1])
    funcIndex = int(sys.argv[2])
    duration = int(sys.argv[3])
    sample_rate = int(sys.argv[4])

    if funcIndex < 0 or funcIndex > 9:
        print("Wrong argument for the generator function!")
        sys.exit()

    frequencies = [int(sys.argv[i]) for i in range(5, len(sys.argv))]

    return filename, funcIndex, duration, sample_rate, frequencies


def generate_data(func_index, frequencies):
    data = None

    if func_index == 0:
        data = sine_wave(frequency=frequencies[0])
    elif func_index == 1:
        data = polyphonic_wave(frequencies=frequencies)
    elif func_index == 2:
        data = chirp_wave(start_freq=frequencies[0], end_freq=frequencies[1])
    elif func_index == 3:
        data = noise()
    elif func_index == 4:
        data = am_wave(carrier_freq=frequencies[0], mod_freq=frequencies[1])
    elif func_index == 5:
        data = fm_wave(carrier_freq=frequencies[0], mod_freq=frequencies[1], mod_index=frequencies[2])
    elif func_index == 6:
        data = segmented_sine_wave(frequencies=frequencies[:-1], segment_duration=frequencies[-1])
    elif func_index == 7:
        data = sine_wave_with_envelope(frequency=frequencies[0])
    elif func_index == 8:
        data = additive_synthesis_wave(fundamental_freq=frequencies[0], num_harmonics=frequencies[1])
    elif func_index == 9:
        data = triangle_wave(frequency=frequencies[0])
    elif func_index == 10:
        data = square_wave(frequency=frequencies[0])

    return data


def save_wave_file(filename, data):
    # 32767 ist die maximale Amplitude, die eine 16-Bit-Audio-Sample haben kann
    scaled = np.int16(data / np.max(np.abs(data)) * 32767)
    write(filename, sample_rate, scaled)


def main():
    global sample_rate, duration
    filename, func_index, duration, sample_rate, frequencies = get_all_arguments()

    # This is the default array for the timestamps
    global timestamps
    timestamps = np.linspace(0, duration, int(sample_rate * duration), endpoint=False)

    data = generate_data(func_index, frequencies)
    save_wave_file(filename, data)

    print("WAV-File was generated and saved.")


if __name__ == '__main__':
    main()