import numpy as np
import pyopencl as cl
import matplotlib.pyplot as plt
import argparse
from scipy.io import wavfile

def read_wav_file(file_path):
    sample_rate, data = wavfile.read(file_path)
    if len(data.shape) > 1:
        data = data[:, 0]  # Falls Stereo, nur einen Kanal verwenden
    return data, sample_rate

def perform_dft(data, block_size, shift_size, threshold):
    platforms = cl.get_platforms()
    devices = platforms[0].get_devices(cl.device_type.GPU)
    units_count = devices[0].max_compute_units

    context = cl.create_some_context()
    queue = cl.CommandQueue(context)

    mf = cl.mem_flags
    data = data.astype(np.float32)
    num_blocks = (len(data) - block_size) // shift_size + 1
    dft_result = np.zeros((num_blocks, block_size // 2), dtype=np.complex64)

    program_source = """
    __kernel void dft_kernel(__global const float *data, __global float2 *result, int count_units, int block_size, int shift_size, int num_blocks) {
        int gid = get_global_id(0);
        int block_start = gid * shift_size;
        if (block_start + block_size > get_global_size(0)) return;

        for (int k = 0; k < block_size / 2; k++) {
            float2 sum = (float2)(0.0f, 0.0f);
            for (int n = 0; n < block_size; n++) {
                float angle = -2.0f * M_PI * k * n / block_size;
                float2 exp_term = (float2)(cos(angle), sin(angle));
                sum += (float2)(data[block_start + n], 0.0f) * exp_term;
            }
            result[gid * block_size / 2 + k] = sum;
        }
    }
    """

    program = cl.Program(context, program_source).build()

    data_buffer = cl.Buffer(context, mf.READ_ONLY | mf.COPY_HOST_PTR, hostbuf=data)
    result_buffer = cl.Buffer(context, mf.WRITE_ONLY, dft_result.nbytes)

    dft_kernel = program.dft_kernel
    dft_kernel.set_args(data_buffer, result_buffer, np.int32(units_count), np.int32(block_size), np.int32(shift_size), np.int32(num_blocks))

    cl.enqueue_nd_range_kernel(queue, dft_kernel, (num_blocks,), None)
    cl.enqueue_copy(queue, dft_result, result_buffer).wait()

    dft_magnitude = np.abs(dft_result)
    # dft_magnitude[dft_magnitude < threshold] = 0

    return np.mean(dft_magnitude, axis=0)

def plot_frequency_spectrum(aggregated_dft, sample_rate, block_size):
    freqs = np.fft.fftfreq(block_size, d=1/sample_rate)[:block_size//2]
    plt.figure(figsize=(10, 6))
    plt.plot(freqs, 20 * np.log10(aggregated_dft))
    plt.xlabel('Frequenz (Hz)')
    plt.ylabel('Amplitude (dB)')
    plt.title('Frequenzspektrum')
    plt.grid(True)
    plt.show()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='DFT Analysis on WAV file using OpenCL')
    parser.add_argument('file_path', type=str, help='Path to the WAV file')
    parser.add_argument('block_size', type=int, help='Block size for DFT')
    parser.add_argument('shift_size', type=int, help='Shift size for DFT')
    parser.add_argument('threshold', type=float, help='Threshold for DFT result')
    args = parser.parse_args()

    data, sample_rate = read_wav_file(args.file_path)
    aggregated_dft = perform_dft(data, args.block_size, args.shift_size, args.threshold)
    plot_frequency_spectrum(aggregated_dft, sample_rate, args.block_size)