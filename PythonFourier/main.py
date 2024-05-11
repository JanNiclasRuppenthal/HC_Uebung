import wave

# Pfad zur WAV-Datei
wav_file = "../resources/Geheimnisvolle_Wellenlaengen.wav"

# Öffne die WAV-Datei im Lesemodus
with wave.open(wav_file, 'rb') as wav:
    # Anzahl der Kanäle (Mono: 1, Stereo: 2 usw.)
    num_channels = wav.getnchannels()
    print("Anzahl der Kanäle:", num_channels)

    # Abtastbreite in Bytes
    sample_width = wav.getsampwidth()
    print("Aufloesung:", sample_width*8, "Bits")

    # Abtastfrequenz
    sample_rate = wav.getframerate()
    print("Abtastfrequenz:", sample_rate, "Hz")

    # Anzahl der Frames insgesamt
    num_frames = wav.getnframes()
    print("Anzahl der Frames:", num_frames)

    # Dauer des Audiosignals in Sekunden
    duration = num_frames / sample_rate
    print("Dauer des Audiosignals:", duration, "Sekunden")

    # Lese die Audiodaten
    audio_data = wav.readframes(num_frames)

# Jetzt hast du die Audiodaten in `audio_data`, und du kannst mit ihnen weiterarbeiten.
