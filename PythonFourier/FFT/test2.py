import sys
import time
import numpy as np
import pyopencl as cl
from scipy.io import wavfile

# OpenCL Kernel zur Durchführung der FFT mit gid-Liste
kernel_code = """
#define len 64   // Wert für N Punkt
#define PI 3.141593f
__kernel void fft(__global float2 *data, const int block_size, __global float2 *output) {
    int gid = get_global_id(0);
    float2 sum = (float2)(0.0f, 0.0f);
    float angle;
    
    for (int k = 0; k < block_size; ++k) {
        angle = -2.0f * PI * gid * k / (float)block_size;
    sum += data[k] * (float2)(cos(angle), sin(angle));
    }
    
    output[gid] += sum;
}
""";


def get_all_arguments():
    file_path = str(sys.argv[1])
    block_size = int(sys.argv[2])

    if block_size < 64:
        block_size = 64
    elif block_size > 512:
        block_size = 512

    shift_size = int(sys.argv[3])
    if shift_size < 1:
        shift_size = 1
    elif shift_size > block_size:
        shift_size = block_size

    threshold = float(sys.argv[4])

    if threshold < 0:
        threshold = 0

    return file_path, block_size, shift_size, threshold


def analyze_wav_file(file_path):
    sample_rate, data = wavfile.read(file_path)

    if len(data.shape) > 1:
        data = data[:, 0]

    return data, sample_rate


def analyze(data, block_size, shift_size):
    num_samples = len(data)
    num_blocks = (num_samples - block_size) // shift_size + 1

    # Initialisiere OpenCL
    platform = cl.get_platforms()[0]
    device = platform.get_devices()[0]
    context = cl.Context([device])
    queue = cl.CommandQueue(context)
    program = cl.Program(context, kernel_code).build()

    # Erstelle Buffers für Daten, output und gid_list
    data_buffer = cl.Buffer(context, cl.mem_flags.READ_WRITE, size=data.nbytes)
    output_buffer = cl.Buffer(context, cl.mem_flags.WRITE_ONLY, size=data.nbytes)
    gid_list_buffer = cl.Buffer(context, cl.mem_flags.WRITE_ONLY, size=num_blocks * np.int32().itemsize)

    # Kopiere Daten auf den Buffer
    cl.enqueue_copy(queue, data_buffer, data)

    # Führe den Kernel aus
    program.fft(queue, (num_blocks,), None, data_buffer, np.int32(block_size), output_buffer)

    # Kopiere die Ergebnisse zurück
    output = np.empty_like(data)
    cl.enqueue_copy(queue, output, output_buffer).wait()

    # Berechne aggregierte FFT
    aggregated_fft = np.zeros(block_size//2)

    # Hier könnte die tatsächliche FFT-Berechnung durchgeführt werden
    # Zum Beispiel: np.fft.fft(output, block_size)

    aggregated_fft /= num_blocks

    return aggregated_fft



def write_data_to_file(data, file_path):
    with open(file_path, 'w') as file:
        for item in data:
            file.write(str(item) + '\n')


def print_run_time(run_time):
    minutes = run_time // 60
    seconds = run_time % 60
    print('Laufzeit: {} Minuten und {:.2f} Sekunden'.format(minutes, seconds))


def main():
    start_time = time.time()

    file_path, block_size, shift_size, threshold = get_all_arguments()
    wav_data, sample_rate = analyze_wav_file(file_path)

    aggregated_fft = analyze(wav_data, block_size, shift_size)

    run_time = time.time() - start_time
    print_run_time(run_time)

    write_data_to_file([sample_rate, block_size, threshold], 'sr_bs_t.txt')
    write_data_to_file(aggregated_fft, 'aggregated_fft.txt')
    write_data_to_file(wav_data, 'wav_data.txt')

    result = [(index * sample_rate / block_size, aggregated_fft[index])
              for index in range(len(aggregated_fft)) if aggregated_fft[index] > threshold]

    print(result)


if __name__ == "__main__":
    main()
