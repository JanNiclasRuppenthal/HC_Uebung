import time
import sys
from scipy.io import wavfile


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

    ''' 
    Falls zwei Kanaele (Stereo) in der WAV-Datei existieren, 
    dann schneiden wir einen Kanal ab, um Rechen- sowie Laufzeit zu sparen.
    '''
    if len(data.shape) > 1:
        data = data[:, 0]

    return data, sample_rate


def write_data_to_file(data, file_path):
    with open(file_path, 'w') as file:
        for item in data:
            file.write(str(item) + '\n')


def write_data_to_files(aggregated_fft, wav_data, sample_rate, block_size, threshold):
    write_data_to_file([sample_rate, block_size, threshold], 'sr_bs_t.txt')
    write_data_to_file(aggregated_fft, 'aggregated_fft.txt')
    write_data_to_file(wav_data, 'wav_data.txt')


def print_run_time(run_time):
    minutes = run_time // 60
    seconds = run_time % 60

    print('Laufzeit: {} Minuten und {:.2f} Sekunden'.format(minutes, seconds))


def print_results(aggregated_fft, sample_rate, block_size, threshold):
    result = [(index * sample_rate / block_size, aggregated_fft[index])
              for index in range(len(aggregated_fft)) if aggregated_fft[index] > threshold]

    print(result)


def main(analyze_method):
    file_path, block_size, shift_size, threshold = get_all_arguments()
    wav_data, sample_rate = analyze_wav_file(file_path)

    start_time = time.time()

    aggregated_fft = analyze_method(wav_data, block_size, shift_size)

    run_time = time.time() - start_time
    print_run_time(run_time)

    # Ab hier soll nicht mehr die Zeit gemessen werden, da ich nur die Zeit fuer eine Fourieranalyse haben moechte
    write_data_to_files(aggregated_fft, wav_data, sample_rate, block_size, threshold)

    print_results(aggregated_fft, sample_rate, block_size, threshold)
