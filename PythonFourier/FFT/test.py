import numpy as np
import pyopencl as cl
import argparse
from scipy.io import wavfile

def read_wav_file(file_path):
    sample_rate, data = wavfile.read(file_path)
    if len(data.shape) > 1:
        data = data[:, 0]  # Falls Stereo, nur einen Kanal verwenden
    return data, sample_rate

def perform_dft(data, block_size, shift_size, threshold):
    context = cl.create_some_context()
    queue = cl.CommandQueue(context)

    mf = cl.mem_flags
    data = data.astype(np.float32)
    num_blocks = (len(data) - block_size) // shift_size + 1
    data_length = np.int32(len(data))  # Länge des Daten-Arrays

    dft_result = np.zeros((num_blocks, block_size // 2), dtype=np.complex64)

    program_source = """
    __kernel void dft_kernel(__global const float *data, __global float2 *result, int data_length, int block_size, int shift_size) {
        int gid = get_global_id(0);
        int block_start = gid * shift_size;
        if (block_start + block_size > data_length) return;

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

    dft_kernel.set_args(data_buffer, result_buffer, data_length, np.int32(block_size), np.int32(shift_size))

    cl.enqueue_nd_range_kernel(queue, dft_kernel, (num_blocks,), None)

    cl.enqueue_copy(queue, dft_result, result_buffer).wait()

    return np.sum(np.abs(dft_result), axis=0) / num_blocks

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='DFT Analysis on WAV file using OpenCL')
    parser.add_argument('file_path', type=str, help='Path to the WAV file')
    parser.add_argument('block_size', type=int, help='Block size for DFT')
    parser.add_argument('shift_size', type=int, help='Shift size for DFT')
    parser.add_argument('threshold', type=float, help='Threshold for DFT result')
    args = parser.parse_args()

    data, sample_rate = read_wav_file(args.file_path)
    aggregated_dft = perform_dft(data, args.block_size, args.shift_size, args.threshold)
    # Hier können Sie mit aggregated_dft weiterarbeiten, z.B. plotten oder speichern
