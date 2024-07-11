import numpy as np
from util import *

# Neu fuer Aufgabe 03
import os
import multiprocessing as mp


def fft_process(id, lock, cpu_count, data, block_size, shift_size, aggregated_fft, result_shape):
    local_fft = np.zeros(result_shape)
    for i in range(id * shift_size, len(data) - block_size + 1, cpu_count * shift_size):
        block = data[i:i+block_size]
        fft_result = np.fft.fft(block)
        local_fft += np.abs(fft_result[:result_shape[0]])

    '''
    Bei der Addition der Ergebnisse muss man darauf achten, dass man diese Operation synchronisiert, da es zu Fehler
    kommen kann (z.B Race Conditions). Deswegen habe ich einen Lock verwendet, sodass die Threads nacheinander die 
    Ergebniss addiert.
    '''
    with lock:
        for i in range(result_shape[0]):
            aggregated_fft[i] += local_fft[i]

def analyze(data, block_size, shift_size):
    num_samples = len(data)
    num_blocks = (num_samples - block_size) // shift_size + 1

    cpu_count = os.cpu_count()
    processes = []
    lock = mp.Lock()

    # Gemeinsames Array, welches die Threads sich teilen
    aggregated_fft = mp.Array('d', block_size//2)

    result_shape = (block_size//2,)

    for id in range(cpu_count):
        process = mp.Process(target=fft_process, args=(id, lock, cpu_count, data, block_size, shift_size, aggregated_fft, result_shape))
        processes.append(process)
        process.start()

    for process in processes:
        process.join()

    aggregated_fft = np.frombuffer(aggregated_fft.get_obj())
    aggregated_fft /= num_blocks

    return aggregated_fft


if __name__ == "__main__":
    main(analyze_method=analyze)