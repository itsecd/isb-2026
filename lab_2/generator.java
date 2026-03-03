import java.io.FileWriter;
import java.io.IOException;
import java.util.Random;

public class RandomGenerator {

    public static void generateAndWriteToFile() {
        long seed = System.currentTimeMillis();
        Random random = new Random(seed);


        try (FileWriter writer = new FileWriter("output_java.txt")) {
            
            for (int i = 0; i < 128; i++) {
                int randomNum = random.nextInt(2);
                
                writer.write(String.valueOf(randomNum));
            }
            
        } catch (IOException e) {
            System.err.println("Ошибка при записи в файл: " + e.getMessage());
        }
    }

    public static void main(String[] args) {
        generateAndWriteToFile();
    }
}