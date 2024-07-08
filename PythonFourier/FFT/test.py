import numpy as np
import pyopencl as cl
import scipy.io.wavfile as wav
import matplotlib.pyplot as plt

# Lade die WAV-Datei
def load_wav(filename):
    sample_rate, data = wav.read(filename)
    return sample_rate, data

def perform_dft(data, block_size, shift_size):
    # Setup OpenCL context and queue
    platform = cl.get_platforms()[0]
    device = platform.get_devices()[0]
    context = cl.Context([device])
    queue = cl.CommandQueue(context)

    mf = cl.mem_flags
    data = data.astype(np.float32)
    data_length = len(data)
    num_blocks = (data_length - block_size) // shift_size + 1

    # Allocate memory on the device
    data_buffer = cl.Buffer(context, mf.READ_ONLY | mf.COPY_HOST_PTR, hostbuf=data)
    result_real_buffer = cl.Buffer(context, mf.WRITE_ONLY, size=(num_blocks * block_size // 2) * np.dtype(np.float32).itemsize)
    result_imag_buffer = cl.Buffer(context, mf.WRITE_ONLY, size=(num_blocks * block_size // 2) * np.dtype(np.float32).itemsize)

    # Build and execute the OpenCL program
    program_source = """
    __kernel void dft_kernel(__global const float *data, __global float *result_real, __global float *result_imag, int data_length, int block_size, int shift_size) {
        int gid = get_global_id(0);
        int block_start = gid * shift_size;

        if (block_start + block_size > data_length) return;

        for (int k = 0; k < block_size / 2; k++) {
            float sum_real = 0.0f;
            float sum_imag = 0.0f;
            for (int n = 0; n < block_size; n++) {
                float angle = -2.0f * M_PI * k * n / block_size;
                float cos_val = cos(angle);
                float sin_val = sin(angle);
                float data_val = data[block_start + n];
                sum_real += data_val * cos_val;
                sum_imag += data_val * sin_val;
            }
            result_real[gid * (block_size / 2) + k] = sum_real;
            result_imag[gid * (block_size / 2) + k] = sum_imag;
        }
    }
    """

    program = cl.Program(context, program_source).build()
    dft_kernel_func = program.dft_kernel
    dft_kernel_func.set_args(data_buffer, result_real_buffer, result_imag_buffer, np.int32(data_length), np.int32(block_size), np.int32(shift_size))

    cl.enqueue_nd_range_kernel(queue, dft_kernel_func, (num_blocks,), None)

    # Read the result back to host
    result_real = np.zeros(num_blocks * (block_size // 2), dtype=np.float32)
    result_imag = np.zeros(num_blocks * (block_size // 2), dtype=np.float32)
    cl.enqueue_copy(queue, result_real, result_real_buffer).wait()
    cl.enqueue_copy(queue, result_imag, result_imag_buffer).wait()

    # Aggregate the results
    dft_result = np.zeros(block_size // 2, dtype=np.complex64)
    for i in range(num_blocks):
        start_index = i * (block_size // 2)
        end_index = (i + 1) * (block_size // 2)
        dft_result += result_real[start_index:end_index] + 1j * result_imag[start_index:end_index]

    aggregated_dft = np.abs(dft_result) / num_blocks

    return aggregated_dft

def main():
    sample_rate, data = load_wav("../wave.wav")

    # Bestimme die Blockgröße und die Schrittweite
    block_size = 512  # oder eine andere geeignete Größe
    shift_size = 1  # Schrittweite für die Blockverschiebung

    # Berechne DFT blockweise mit OpenCL
    result = perform_dft(data, block_size, shift_size)

    # Plot the result
    plt.plot(result)
    plt.title("Blockwise DFT of WAV file")
    plt.xlabel("Frequency (Hz)")
    plt.ylabel("Magnitude")
    plt.show()

if __name__ == "__main__":
    main()
