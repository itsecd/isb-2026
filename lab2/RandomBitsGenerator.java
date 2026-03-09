import java.io.FileWriter;
import java.io.IOException;
import java.util.Random;

public class RandomBitsGenerator {
    public static void main(String[] args) {
        try {
            Random random = new Random();
            StringBuilder gen = new StringBuilder(128);
            for (int i = 0; i < 128; i++) {
                gen.append(random.nextInt(2));
            }
            try (FileWriter writer = new FileWriter("out_java.txt")) {
                writer.write(gen.toString());
            }
        } catch (IOException e) {
            System.err.println("Ошибка записи: " + e.getMessage());
            System.exit(1);
        }
    }
}