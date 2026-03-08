import java.io.FileWriter;
import java.io.IOException;
import java.util.Random;

public class PRNG {
    public static void generateRandomSequence(String path) {
        Random random = new Random();
        StringBuilder seq = new StringBuilder(128);

        for (int i = 0; i < 128; i++) {
            seq.append(random.nextInt(2));
        }

        try (FileWriter fileWriter = new FileWriter(path)) {
            fileWriter.write(seq.toString());
        } catch (IOException e) {
            e.printStackTrace();
        }
    }
    public static void main(String[] args) {
        generateRandomSequence("seq_generator_java.txt");
    }
}