import numpy as np
from util import *

def analyze(data, block_size, shift_size):
    num_samples = len(data)
    num_blocks = (num_samples - block_size) // shift_size + 1

    aggregated_fft = np.zeros(block_size//2, dtype=float) #Redundanz der Spiegelung entfernen

    # Fuer jeden Datenblock wird die jeweilige ausgewaehlte Funktion angewendet.
    for i in range(0, len(data) - block_size + 1, shift_size):
        block = data[i:i+block_size]
        fft_result = np.fft.fft(block)
        '''
        Summiere alle Ergebnisse auf.
        Wir verwenden den Absolutbetrag der Ergebnisse, da diese komplexe Zahlen sind.
        Der Betrag einer komplexen Zahl ist die Entfernung der Zahl zum Nullpunkt im komplexen Raum.
        '''
        aggregated_fft += np.abs(fft_result[:block_size//2])

    # Wir berechnen den Mittelwert, da die Summen sonst zu gross sind
    aggregated_fft /= num_blocks

    return aggregated_fft


if __name__ == "__main__":
    main(analyze_method=analyze)
