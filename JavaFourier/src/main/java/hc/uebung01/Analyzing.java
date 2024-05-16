package hc.uebung01;

import java.io.BufferedReader;
import java.io.FileReader;
import java.io.IOException;
import java.util.ArrayList;
import java.util.List;

public class Analyzing
{
    public static void main(String[] args) throws IOException
    {
        int[] smallData = readDataToArray();
        List<Double> aggregated_fft = readDataToList();


        int sample_rate = smallData[0];
        int block_size = smallData[1];

        List<Integer> peaksIndices = getPeaks(aggregated_fft);
        List<Double> main_frequencies = getMainFrequencies(peaksIndices, sample_rate, block_size);

        List<Double> frequency_axis = new ArrayList<>();
        for (int index = 0; index < aggregated_fft.size(); index++)
        {
            frequency_axis.add((double) (index * sample_rate / block_size));
        }


        // print the results:
        for (int index = 0; index < peaksIndices.size(); index++)
        {
            int peak = peaksIndices.get(index);
            System.out.printf("Main Frequency %f with amplitude %f at index %d\n", main_frequencies.get(index), aggregated_fft.get(peak), peak);
        }



    }

    private static int[] readDataToArray()
    {
        int[] data = new int[2];
        try (BufferedReader br = new BufferedReader(new FileReader("sample_rate_and_block_size.txt")))
        {
            for (int index = 0; index < 2; index++)
            {
                data[index] = Integer.parseInt(br.readLine());
            }
        } catch (IOException e)
        {
            throw new RuntimeException(e);
        }


        return data;
    }


    private static List<Double> readDataToList()
    {
        List<Double> data = new ArrayList<Double>();
        try (BufferedReader br = new BufferedReader(new FileReader("aggregated_fft.txt")))
        {
            String line;
            while ((line = br.readLine()) != null)
            {
                data.add(Double.parseDouble(line));
            }
        } catch (IOException e)
        {
            throw new RuntimeException(e);
        }


        return data;
    }


    private static List<Integer> getPeaks(List<Double> data)
    {
        List<Integer> peaks = new ArrayList<>();

        for (int index = 1; index < data.size(); index++)
        {
            if (data.get(index) > data.get(index - 1) && data.get(index) > data.get(index + 1))
            {
                peaks.add(index);
            }
        }


        return peaks;
    }

    private static List<Double> getMainFrequencies(List<Integer> peaks, int sampleRate, int blockSize)
    {
        List<Double> main_frequencies = new ArrayList<>();

        for (int index : peaks)
        {
            main_frequencies.add((double) index * sampleRate / blockSize);
        }

        return main_frequencies;
    }
}
