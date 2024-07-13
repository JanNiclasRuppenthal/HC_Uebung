import numpy as np
from numba import cuda, float32
import math
from util import *

@cuda.jit
def fft(input_signal, window_size, step_size, output_fft):
    idx = cuda.grid(1)
    if idx * step_size + window_size < input_signal.size:
        windowed_signal = input_signal[idx * step_size: idx * step_size + window_size]

        N = window_size
        for k in range(N):
            real_sum = 0.0
            imag_sum = 0.0
            for n in range(N):
                angle = -2.0 * math.pi * k * n / N
                real_sum += windowed_signal[n] * math.cos(angle)
                imag_sum -= windowed_signal[n] * math.sin(angle)
            output_fft[idx, k] = math.sqrt(real_sum**2 + imag_sum**2)


def analyze(data, block_size, shift_size):
    num_blocks = (len(data) - block_size) // shift_size + 1
    output_fft = np.zeros((num_blocks, block_size), dtype=np.float32)

    # Daten auf die GPU laden
    d_input_signal = cuda.to_device(data.astype(np.float32))
    d_output_fft = cuda.to_device(output_fft)

    threads_per_block = 128
    blocks_per_grid = (num_blocks + (threads_per_block - 1)) // threads_per_block

    # Starte den Kernel auf der Nvidia GPU
    fft[blocks_per_grid, threads_per_block](d_input_signal, block_size, shift_size, d_output_fft)

    #Warte bis die Berechnung im Kernel fertig ist
    cuda.synchronize()
    aggregated_fft = d_output_fft.copy_to_host()

    aggregated_fft = np.sum(aggregated_fft, axis=0) / num_blocks

    return aggregated_fft

if __name__ == "__main__":
    main(analyze_method=analyze)
