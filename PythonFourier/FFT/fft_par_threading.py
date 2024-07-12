import numpy as np

from util import *

# Neu fuer Aufgabe 03
import os
import threading

def fft_thread(id, lock, cpu_count, data, block_size, shift_size, aggregated_fft):
    local_fft = np.zeros(block_size//2)
    for i in range(id * shift_size, len(data) - block_size + 1, cpu_count * shift_size):
        block = data[i:i+block_size]
        fft_result = np.fft.fft(block)
        local_fft += np.abs(fft_result[:block_size//2])

    '''
    Bei der Addition der Ergebnisse muss man darauf achten, dass man diese Operation synchronisiert, da es zu Fehler
    kommen kann (z.B Race Conditions). Deswegen habe ich einen Lock verwendet, sodass die Threads nacheinander die 
    Ergebniss addiert.
    '''
    lock.acquire()
    aggregated_fft += local_fft
    lock.release()


def analyze(data, block_size, shift_size):
    num_samples = len(data)
    num_blocks = (num_samples - block_size) // shift_size + 1

    cpu_count = os.cpu_count()
    print("#Prozessoren: %s" % cpu_count)
    threads = []
    lock = threading.Lock()
    aggregated_fft = np.zeros(block_size//2)

    for id in range(cpu_count):
        thread = threading.Thread(target=fft_thread, args=(id, lock, cpu_count, data, block_size, shift_size, aggregated_fft))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    aggregated_fft /= num_blocks

    return aggregated_fft


if __name__ == "__main__":
    main(analyze_method=analyze)
