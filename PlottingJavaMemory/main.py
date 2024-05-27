import pandas as pd
import matplotlib.pyplot as plt


def plot_data(data, title):
    plt.figure(figsize=(10, 6))
    plt.plot(data, marker='o', linestyle='-')
    plt.title(title)
    plt.xlabel('Datenpunkte')
    plt.ylabel('Speicher in MB')
    plt.grid(True)
    plt.show()

def main():
    dataframe = pd.read_csv('CSVresources/Speicher_Java_LinuxMint.csv')
    memoryLinuxMint = dataframe.iloc[:-1, 1] # Verwende nicht den letzten Wert, da er negativ sein kann!

    dataframe = pd.read_csv('CSVresources/Speicher_Java_Pi.csv')
    memoryPi = dataframe.iloc[:-1, 1]

    dataframe = pd.read_csv('CSVresources/Speicher_Java_Windows.csv')
    memoryWindows = dataframe.iloc[:-1, 1]


    #plot the data
    plot_data(memoryWindows/10**6, 'Speicherverbrauch im Heap (Windows)')
    plot_data(memoryPi/10**6, 'Speicherverbrauch im Heap (Raspberry Pi)')
    plot_data(memoryLinuxMint/10**6, 'Speicherverbrauch im Heap (Linux Mint)')


if __name__ == '__main__':
    main()
