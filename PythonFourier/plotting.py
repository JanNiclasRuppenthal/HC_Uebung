import numpy as np
import matplotlib.pyplot as plt

def plot_data(filename):
    # Daten aus der Datei lesen
    data = np.loadtxt(filename)

    # Diagramm erstellen
    plt.plot(data)
    plt.xlabel('Frequenz / Phase')
    plt.ylabel('Wert')
    plt.title('Daten aus ' + filename)
    plt.grid(True)
    plt.show()

def main():
    # Dateinamen
    amplitude_mean_file = "amplitude_mean.txt"
    amplitude_std_deviation_file = "amplitude_std_deviation.txt"
    phase_mean_file = "phase_mean.txt"
    phase_std_deviation_file = "phase_std_deviation.txt"

    # Daten plotten
    plot_data(amplitude_mean_file)
    plot_data(amplitude_std_deviation_file)
    plot_data(phase_mean_file)
    plot_data(phase_std_deviation_file)

if __name__ == "__main__":
    main()