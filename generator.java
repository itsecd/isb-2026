import java.io.FileWriter;
import java.io.IOException;
import java.util.Random;

public class Generator {
    public static void main(String[] args) {
        try (FileWriter writer = new FileWriter(Constants.OUTPUT_FILENAME)) {
            Random rand = new Random();
            
            for (int i = 0; i < Constants.SEQUENCE_LENGTH; i++) {
                writer.write(rand.nextInt(2) + "");
            }
            
        } catch (IOException e) {
            System.out.println("Ошибка: " + e.getMessage());
        }
    }
}