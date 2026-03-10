import java.io.FileWriter;
import java.io.IOException;
import java.util.Random;

public class JavaGenerator {
    public static void main(String[] args) {
        try {
            FileWriter writer = new FileWriter("sequence_java.txt");
            Random rand = new Random();
            int N = 128;

            for (int i = 0; i < N; i++) {
                writer.write(rand.nextInt(2) + "");
            }
            writer.close();
            System.out.println("The Java sequence is stored in sequence_java.txt");
        } catch (IOException e) {
            e.printStackTrace();
        }
    }
}