package hc.uebung01;

import org.apache.commons.math3.complex.Complex;
import org.apache.commons.math3.transform.DftNormalization;
import org.apache.commons.math3.transform.FastFourierTransformer;
import org.apache.commons.math3.transform.TransformType;

import javax.sound.sampled.*;
import java.io.File;
import java.io.FileWriter;
import java.io.IOException;
import java.nio.file.Paths;
import java.util.Arrays;


public class Main {

    public static void main(String[] args) {
        if (args.length < 2)
        {
            System.err.println("Usage: java Main <input_file> <block_size>");
            return;
        }

        String filePath = args[0];
        int blockSize = Integer.parseInt(args[1]);
        String algorithm_option = (args.length > 2) ?  args[2] : "";

        long startTime = System.currentTimeMillis();

        try
        {
            System.out.printf("Analyzing %s!\n", filePath);
            double[] wavData = analyzeWavFile(filePath);
            int sampleRate = getSampleRate(filePath);

            System.out.println("Fourieranalysis!");
            double[] aggregatedFFT = analyze(wavData, blockSize, algorithm_option);

            System.out.println("Write results in aggregated_fft.txt");
            writeSampleRateAndBlockSizeToFile("sample_rate_and_block_size.txt", sampleRate, blockSize);
            writeDataToFile("aggregated_fft.txt", aggregatedFFT, blockSize);
        } catch (IOException e)
        {
            e.printStackTrace();
        } catch (UnsupportedAudioFileException e)
        {
            throw new RuntimeException(e);
        }

        long runTime = System.currentTimeMillis() - startTime;
        System.out.printf("Laufzeit: %d Minuten und %.2f Sekunden%n", runTime / 60000, (runTime % 60000) / 1000.0);
    }

    public static double[] analyzeWavFile(String filePath) throws IOException, UnsupportedAudioFileException {
        AudioInputStream audioInputStream = AudioSystem.getAudioInputStream(new File(filePath));
        AudioFormat format = audioInputStream.getFormat();
        boolean isStereo = format.getChannels() > 1;

        int numBytes = (int) (audioInputStream.getFrameLength() * format.getFrameSize());
        byte[] audioBytes = new byte[numBytes];
        audioInputStream.read(audioBytes);

        int numSamples = numBytes / 2; // Jedes Sample ist 2 Bytes (fuer 16-bit Audio)
        if (isStereo)
        {
            numSamples /= 2; // Bei Stereo: halbiere die Anzahl der Samples, um nur einen Kanal zu beruecksichtigen
        }

        double[] audioData = new double[numSamples];
        boolean isBigEndian = format.isBigEndian();

        for (int byteIndex = 0, sampleIndex = 0; byteIndex < numBytes; byteIndex += 4, sampleIndex++) { // byteIndex+=4, da wir nur jeden zweiten Sample (einen Kanal) nehmen
            int sample = 0;
            if (isBigEndian)
            {
                sample = (audioBytes[byteIndex] << 8) | (audioBytes[byteIndex + 1] & 0xFF);
            } else
            {
                sample = (audioBytes[byteIndex + 1] << 8) | (audioBytes[byteIndex] & 0xFF);
            }
            audioData[sampleIndex] = sample; // / 32768.0 -> Konvertiere zu Bereich -1.0 bis 1.0 fuer 16-bit signed
        }

        return audioData;
    }

    public static int getSampleRate(String filePath) throws IOException, UnsupportedAudioFileException {
        AudioInputStream audioInputStream = AudioSystem.getAudioInputStream(Paths.get(filePath).toFile());
        return (int) audioInputStream.getFormat().getSampleRate();
    }

    public static double[] analyze(double[] data, int blockSize, String algorithm_option)
    {
        int numSamples = data.length;
        int numBlocks = numSamples - blockSize + 1;

        double[] aggregatedFFT = new double[blockSize / 2]; // Redundanz der Spiegelung entfernen
        double[] block = new double[blockSize];

        // Fuer jeden Datenblock wird die FFT berechnet
        for (int i = 0; i < numBlocks; i++)
        {
            System.arraycopy(data, i, block, 0, blockSize);

            Complex[] fftResult;

            if (algorithm_option.equals("dft"))
            {
                fftResult = dft(block);
            }
            else if (algorithm_option.equals("rec_fft"))
            {
                Complex[] temp = new Complex[blockSize];
                for (int j = 0; j < blockSize; j++)
                {
                    temp[j] = new Complex(block[j], 0);
                }
                fftResult = fft(temp);
            }
            else
            {
                fftResult = fftTransformer(block);
            }




            // Summiere die Ergebnisse auf
            for (int j = 0; j < blockSize / 2; j++)
            {
                aggregatedFFT[j] += fftResult[j].abs();
            }
        }

        // Berechne den Mittelwert
        for (int i = 0; i < blockSize / 2; i++)
        {
            aggregatedFFT[i] /= numBlocks;
        }

        return aggregatedFFT;
    }

    public static Complex[] fftTransformer(double[] dataBlock) {
        FastFourierTransformer transformer = new FastFourierTransformer(DftNormalization.STANDARD);
        return transformer.transform(dataBlock, TransformType.FORWARD);
    }

    public static Complex[] fft(Complex[] dataBlock)
    {
        int N = dataBlock.length;

        // Basisfall der Rekursion: wenn die Eingabelaenge 1 ist, gibt einfach x zurueck
        if (N <= 1) return dataBlock;

        // Teilen der Eingabe in gerade und ungerade Indizes
        Complex[] even = new Complex[N / 2];
        Complex[] odd = new Complex[N / 2];

        for (int i = 0; i < N / 2; i++) {
            even[i] = dataBlock[2 * i];
            odd[i] = dataBlock[2 * i + 1];
        }

        // Rekursive Aufrufe fuer gerade und ungerade Teile
        Complex[] q = fft(even);
        Complex[] r = fft(odd);

        // Kombinieren der Ergebnisse
        Complex[] y = new Complex[N];
        for (int k = 0; k < N / 2; k++) {
            double angle = -2 * Math.PI * k / N;
            Complex wk = new Complex(Math.cos(angle), Math.sin(angle)).multiply(r[k]);
            y[k] = q[k].add(wk);
            y[k + N / 2] = q[k].subtract(wk);
        }

        return y;
    }

    public static Complex[] dft(double[] dataBlock)
    {
        int N = dataBlock.length;
        Complex[] X = new Complex[N];
        Arrays.fill(X, new Complex(0, 0));  // Fuellen Sie das Array mit Null-Komplexzahlen

        for (int k = 0; k < N; k++) {
            Complex sum = new Complex(0, 0);
            for (int n = 0; n < N; n++) {
                double angle = -2 * Math.PI * k * n / N;
                Complex exp = new Complex(Math.cos(angle), Math.sin(angle));  // exponent of complex number is exp(x) = cos(x) + i*sin(x)
                Complex data = new Complex(dataBlock[n], 0);
                sum = sum.add(data.multiply(exp));
            }
            X[k] = sum;
        }
        return X;
    }

    public static void writeDataToFile(String filename, double[] data, int blockSize) {
        try (FileWriter writer = new FileWriter(filename))
        {
            // Schreibe die aggregierten FFT-Daten in die Datei
            for (int i = 0; i < blockSize / 2; i++)
            {
                writer.write(data[i] + "\n");
            }
        } catch (IOException e)
        {
            e.printStackTrace();
        }
    }


    public static void writeSampleRateAndBlockSizeToFile(String filename, int sampleRate, int blockSize) {
        try (FileWriter writer = new FileWriter(filename))
        {
            writer.write(sampleRate  +"\n");
            writer.write(blockSize + "\n");
        } catch (IOException e)
        {
            throw new RuntimeException(e);
        }
    }
}
