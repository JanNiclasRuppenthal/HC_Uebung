import numpy as np
import pyopencl as cl
from util import *


def analyze(data, block_size, shift_size):
    platforms = cl.get_platforms()
    devices = platforms[0].get_devices(cl.device_type.GPU)
    units_count = devices[0].max_compute_units

    context = cl.create_some_context()
    queue = cl.CommandQueue(context)

    mf = cl.mem_flags
    data = data.astype(np.float32)
    num_blocks = (len(data) - block_size) // shift_size + 1
    max_limit = min(200000, num_blocks)

    program_source = """
    __kernel void dft_kernel(__global const float *data, __global float *result, int count_units, int block_size, int shift_size, int num_blocks, int data_length, int index, int max_limit) {
        int gid = get_global_id(0);
        int block_start = (gid + index * max_limit) * shift_size;
        if (block_start + block_size > data_length) return;
        
        for (int k = 0; k < block_size/2; k++) {
            float sum_real = 0.0f;
            float sum_img = 0.0f;
            for (int n = 0; n < block_size; n++) {
                double angle = -2.0f * M_PI * k * n / block_size;
                sum_real += data[block_start + n] * cos(angle);
                sum_img -= data[block_start + n] * sin(angle);
            }
            result[gid * block_size/2 + k] = sqrt(sum_real * sum_real + sum_img * sum_img);
            
        }       
    }
    """

    program = cl.Program(context, program_source).build()
    dft_kernel = program.dft_kernel

    index = 0
    aggregated_dft = np.zeros(block_size // 2, dtype=np.float32)
    num_blocks_temp = num_blocks
    while max_limit != 0:
        dft_result = np.zeros((max_limit, block_size // 2), dtype=np.float32)
        data_buffer = cl.Buffer(context, mf.READ_ONLY | mf.COPY_HOST_PTR, hostbuf=data)
        result_buffer = cl.Buffer(context, mf.WRITE_ONLY, dft_result.nbytes)

        dft_kernel.set_args(data_buffer, result_buffer, np.int32(units_count), np.int32(block_size),
                            np.int32(shift_size), np.int32(num_blocks), np.int32(len(data)), np.int32(index),
                            np.int32(max_limit))

        cl.enqueue_nd_range_kernel(queue, dft_kernel, (max_limit,), None)
        cl.enqueue_copy(queue, dft_result, result_buffer).wait()

        aggregated_dft += np.sum(dft_result, axis=0)

        index += 1
        num_blocks_temp -= max_limit
        max_limit = min(max_limit, num_blocks_temp)

    aggregated_dft /= num_blocks

    return aggregated_dft


if __name__ == "__main__":
    main(analyze_method=analyze)