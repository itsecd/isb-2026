import java.io.FileWriter;
import java.io.IOException;
import java.util.Random;

public class Generator {
    static String FILE_PATH = "../sequences/java_seq.txt";

    public static void main(String[] args) {
        int size = 128;
        int[] sequence = new int[size];
        Random rd = new Random();
        
        for (int i = 0; i < size; i++) {
            sequence[i] = rd.nextInt(2);
        }

        try (FileWriter writer = new FileWriter(FILE_PATH)) {
            for (int i = 0; i < size; i++) {
                writer.write(String.valueOf(sequence[i]));
            }
        } catch (IOException e) {
            System.err.println("Error: " + e.getMessage());
        }
    }
}