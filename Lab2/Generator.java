import java.io.FileWriter;
import java.io.IOException;
import java.util.Random;

public class Generator {
    public static void main(String[] args) {
        Random random = new Random();

        try (FileWriter writer = new FileWriter(Constants.FILENAME)) {
            for (int i = 0; i < Constants.BIT; i++) {
                int bit = random.nextInt(2);
                writer.write(Integer.toString(bit));
            }
        } catch (IOException e) {
            System.err.println("Ошибка при записи файла: " + e.getMessage());
        }
    }
}