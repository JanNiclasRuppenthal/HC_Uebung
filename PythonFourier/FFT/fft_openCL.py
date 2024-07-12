import numpy as np
import pyopencl as cl
from util import *


def analyze(data, block_size, shift_size):
    platforms = cl.get_platforms()
    devices = platforms[0].get_devices(cl.device_type.GPU)
    units_count = devices[0].max_compute_units
    print("#Recheneinheiten: %s" % units_count)

    context = cl.create_some_context()
    queue = cl.CommandQueue(context)

    mf = cl.mem_flags
    data = data.astype(np.float32)
    num_blocks = (len(data) - block_size) // shift_size + 1
    max_limit = min(4000000, num_blocks)

    program_source = """
    __kernel void fft_kernel(__global const float *data, __global float *result, int block_size, int shift_size, int data_length) {
        int gid = get_global_id(0);
        int block_start = gid * shift_size;
        if (block_start + block_size > data_length) return;

        for (int k = 0; k < block_size/2; k++) {
            float sum_real = 0.0f;
            float sum_img = 0.0f;
            for (int n = 0; n < block_size; n++) {
                float angle = -2.0f * M_PI * k * n / block_size;
                sum_real += data[block_start + n] * cos(angle);
                sum_img -= data[block_start + n] * sin(angle);
            }
            result[gid * block_size/2 + k] = sqrt(sum_real * sum_real + sum_img * sum_img);
        }
    }
    """

    program = cl.Program(context, program_source).build()
    fft_kernel = program.fft_kernel

    aggregated_fft = np.zeros(block_size // 2, dtype=np.float32)
    start = 0
    num_blocks_temp = num_blocks
    while num_blocks_temp > 0:
        current_limit = min(max_limit, num_blocks_temp)
        fft_result = np.zeros((current_limit, block_size // 2), dtype=np.float32)
        data_buffer = cl.Buffer(context, mf.READ_ONLY | mf.COPY_HOST_PTR, hostbuf=data[start:start + current_limit * shift_size + block_size])
        result_buffer = cl.Buffer(context, mf.WRITE_ONLY, fft_result.nbytes)

        fft_kernel.set_args(data_buffer, result_buffer, np.int32(block_size),
                            np.int32(shift_size), np.int32(len(data[start:start + current_limit * shift_size + block_size])))

        cl.enqueue_nd_range_kernel(queue, fft_kernel, (current_limit,), None)
        cl.enqueue_copy(queue, fft_result, result_buffer).wait()

        aggregated_fft += np.sum(fft_result, axis=0)

        num_blocks_temp -= current_limit
        start += current_limit * shift_size

    aggregated_fft /= num_blocks

    return aggregated_fft


if __name__ == "__main__":
    main(analyze_method=analyze)