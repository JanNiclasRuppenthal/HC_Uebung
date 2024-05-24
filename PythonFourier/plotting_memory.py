import matplotlib.pyplot as plt
import numpy as np


def read_data_as_np_array(filename):
    return np.loadtxt(filename)

def plot_data(memory, ylabel):
    plt.plot(memory)
    plt.xlabel('Iteration')
    plt.ylabel(ylabel)
    plt.title('Speicherbedarf ueber die gesamten Iterationen')
    plt.show()


if __name__ == '__main__':
    current = read_data_as_np_array('currentMB.txt')
    peak = read_data_as_np_array('peakMB.txt')

    print(np.average(current))

    plot_data(current, "Momentaner Speicherbedarf (MB)")
    plot_data(peak, "Hoechster Speicherbedarf (MB)")