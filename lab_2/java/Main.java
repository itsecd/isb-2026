import java.io.FileWriter;
import java.io.IOException;

public class Main {

    public static void main(String[] args) throws IOException {

        String sequence = Generator.generate(128);

        FileWriter writer = new FileWriter("results.txt");

        writer.write(sequence + "\n\n");

        writer.close();

        System.out.println("Results saved to results.txt");
    }
}