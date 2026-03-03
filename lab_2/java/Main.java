import java.io.FileWriter;
import java.io.IOException;

public class Main {

    public static void main(String[] args) throws IOException {

        String sequence = Generator.generate(128);

        double p1 = NistTests.frequencyTest(sequence);
        double p2 = NistTests.runsTest(sequence);
        double p3 = NistTests.longestRunTest(sequence);

        FileWriter writer = new FileWriter("results.txt");

        writer.write("Sequence:\n" + sequence + "\n\n");

        writer.write("Frequency Test: " + p1 + "\n");
        writer.write("Runs Test: " + p2 + "\n");
        writer.write("Longest Run Test: " + p3 + "\n");

        writer.close();

        System.out.println("Results saved to results.txt");
    }
}