import java.util.Random;
import java.io.BufferedWriter;
import java.io.FileWriter;
import java.io.IOException;

public class generator_java {

    private static final int LENGTH = 128;

    private static String createSequence() {

        Random rng = new Random();
        StringBuilder sequence = new StringBuilder(LENGTH);

        for (int i = 0; i < LENGTH; i++) {
            int bit = rng.nextBoolean() ? 1 : 0;
            sequence.append(bit);
        }

        return sequence.toString();
    }

    private static void saveToFile(String data) throws IOException {

        BufferedWriter writer = new BufferedWriter(new FileWriter("seq_java.txt"));
        writer.write(data);
        writer.close();
    }

    public static void main(String[] args) {

        try {

            String seq = createSequence();
            saveToFile(seq);

        } catch (IOException e) {
            System.out.println("File write error");
        }
    }
}
