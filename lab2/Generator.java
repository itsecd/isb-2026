import java.io.FileWriter;
import java.io.IOException;
import java.util.Random;

public class Generator {
    public static void main(String[] args) {
        try (FileWriter writer = new FileWriter("sequence_java.txt")) {
            Random random = new Random();
            for (int i = 0; i < 128; i++) {
                writer.write(String.valueOf(random.nextInt(2)));
            }
        } catch (IOException e) {
            // Исключение перехватывается без вывода в консоль
        }
    }
}