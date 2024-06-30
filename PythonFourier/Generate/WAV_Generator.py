import numpy as np
from scipy.io.wavfile import write

def generate_sine_wave(frequency, duration, sample_rate):
    t = np.linspace(0, duration, int(sample_rate * duration), endpoint=False)
    return 0.5 * np.sin(2 * np.pi * frequency * t)

def generate_combined_wave(frequencies, duration, sample_rate):
    t = np.linspace(0, duration, int(sample_rate * duration), endpoint=False)
    signal = np.zeros_like(t)
    for frequency in frequencies:
        signal += 0.5 * np.sin(2 * np.pi * frequency * t)
    return signal

def generate_chirp_wave(start_freq, end_freq, duration, sample_rate):
    t = np.linspace(0, duration, int(sample_rate * duration), endpoint=False)
    return 0.5 * np.sin(2 * np.pi * (start_freq + (end_freq - start_freq) * t / duration) * t)

def generate_noise(duration, sample_rate):
    return 0.5 * np.random.normal(0, 1, int(sample_rate * duration))

def save_wave_file(filename, data, sample_rate):
    scaled = np.int16(data / np.max(np.abs(data)) * 32767)
    write(filename, sample_rate, scaled)

# Parameter
sample_rate = 44100  # 44.1 kHz
duration = 5  # 5 seconds

# Generieren und Speichern der WAV-Dateien
sine_wave = generate_sine_wave(440, duration, sample_rate)
save_wave_file("../sine_wave_440Hz.wav", sine_wave, sample_rate)

combined_wave = generate_combined_wave([440, 880, 1760], duration, sample_rate)
save_wave_file("../combined_wave.wav", combined_wave, sample_rate)

chirp_wave = generate_chirp_wave(20, 20000, duration, sample_rate)
save_wave_file("../chirp_wave.wav", chirp_wave, sample_rate)

noise = generate_noise(duration, sample_rate)
save_wave_file("../noise.wav", noise, sample_rate)

def generate_am_wave(carrier_freq, mod_freq, duration, sample_rate):
    t = np.linspace(0, duration, int(sample_rate * duration), endpoint=False)
    carrier = np.sin(2 * np.pi * carrier_freq * t)
    modulator = 1 + 0.5 * np.sin(2 * np.pi * mod_freq * t)
    return 0.5 * carrier * modulator

# Generieren und Speichern der WAV-Datei
am_wave = generate_am_wave(440, 10, duration, sample_rate)
save_wave_file("../am_wave.wav", am_wave, sample_rate)


def generate_fm_wave(carrier_freq, mod_freq, mod_index, duration, sample_rate):
    t = np.linspace(0, duration, int(sample_rate * duration), endpoint=False)
    return 0.5 * np.sin(2 * np.pi * carrier_freq * t + mod_index * np.sin(2 * np.pi * mod_freq * t))

# Generieren und Speichern der WAV-Datei
fm_wave = generate_fm_wave(440, 10, 5, duration, sample_rate)
save_wave_file("../fm_wave.wav", fm_wave, sample_rate)



def generate_polyphonic_wave(frequencies, duration, sample_rate):
    t = np.linspace(0, duration, int(sample_rate * duration), endpoint=False)
    signal = np.zeros_like(t)
    for frequency in frequencies:
        signal += 0.5 * np.sin(2 * np.pi * frequency * t)
    return signal

# Beispiel: Polyphones Signal mit 440 Hz, 880 Hz und 1320 Hz
polyphonic_wave = generate_polyphonic_wave([440, 880, 1320], duration, sample_rate)
save_wave_file("../polyphonic_wave.wav", polyphonic_wave, sample_rate)

def generate_segmented_sine_wave(frequencies, segment_duration, sample_rate):
    signal = np.array([])
    for frequency in frequencies:
        t = np.linspace(0, segment_duration, int(sample_rate * segment_duration), endpoint=False)
        segment = 0.5 * np.sin(2 * np.pi * frequency * t)
        signal = np.concatenate((signal, segment))
    return signal

# Beispiel: Segmente mit 440 Hz, 880 Hz und 1320 Hz
segmented_sine_wave = generate_segmented_sine_wave([440, 880, 1320], duration / 3, sample_rate)
save_wave_file("../segmented_sine_wave.wav", segmented_sine_wave, sample_rate)

def generate_sine_wave_with_envelope(frequency, duration, sample_rate, envelope):
    t = np.linspace(0, duration, int(sample_rate * duration), endpoint=False)
    sine_wave = 0.5 * np.sin(2 * np.pi * frequency * t)
    return sine_wave * envelope

# Beispiel: Sinuswelle mit 440 Hz und einer linearen Hüllkurve
envelope = np.linspace(0, 1, int(sample_rate * duration))
sine_wave_with_envelope = generate_sine_wave_with_envelope(440, duration, sample_rate, envelope)
save_wave_file("../sine_wave_with_envelope.wav", sine_wave_with_envelope, sample_rate)

def generate_additive_synthesis_wave(fundamental_freq, num_harmonics, duration, sample_rate):
    t = np.linspace(0, duration, int(sample_rate * duration), endpoint=False)
    signal = np.zeros_like(t)
    for i in range(1, num_harmonics + 1):
        signal += (0.5 / i) * np.sin(2 * np.pi * fundamental_freq * i * t)
    return signal

# Beispiel: Additive Synthese mit Grundfrequenz 440 Hz und 5 Harmonischen
additive_wave = generate_additive_synthesis_wave(440, 5, duration, sample_rate)
save_wave_file("../additive_wave.wav", additive_wave, sample_rate)


print("WAV-Dateien wurden generiert und gespeichert.")
