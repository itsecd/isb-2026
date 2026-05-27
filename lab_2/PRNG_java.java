import java.io.FileWriter;
import java.io.IOException;
import java.util.Random;

public class PRNG_java {
    public static void main(String[] args) {
        int size = 128;
        int[] sequence = new int[size];
        Random random = new Random();
        
        for (int i = 0; i < size; i++) {
            sequence[i] = random.nextInt(2);
        }
        
        try (FileWriter writer = new FileWriter("lab_2/java_sequence.txt")) {
            for (int num : sequence) {
                writer.write(String.valueOf(num));
            }
        } catch (IOException e) {
            System.err.println("Error: " + e.getMessage());
        }
    }
}