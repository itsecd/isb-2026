import java.io.FileWriter;
import java.io.IOException;
import java.util.Random;

public class Generator_Java {

    public static String generate_sequence(int size) {
        Random random = new Random();
        StringBuilder sequence = new StringBuilder();

        for (int i = 0; i < size; i++) {
            sequence.append(random.nextInt(2));
        }
        return sequence.toString();
    }

    public static void save_to_file(String filename, String data) throws IOException {
        try (FileWriter writer = new FileWriter(filename)) {
            writer.write(data);
        }
    }

    public static void main(String[] args) {
        int length = 128;
        try {
            String sequence = generate_sequence(length);
            save_to_file("java_sequence.txt", sequence);
            System.out.println("Java sequence successfully generated");
        } catch (IOException e) {
            System.err.println("Error writing file: " + e.getMessage());
        }
    }
}