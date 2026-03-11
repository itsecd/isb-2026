import java.io.FileWriter;
import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Paths;
import java.util.Random;

public class Generate {
    public static void main(String[] args) {
        int LENGTH = 128;
        Random rand = new Random();
        String outputPath = "../sequences/sequence_java.txt";
        
        try {
            Files.createDirectories(Paths.get("sequences"));
        } catch (IOException e) {
            System.err.println("Ошибка создания директории: " + e.getMessage());
            return;
        }
        
        try (FileWriter file = new FileWriter(outputPath)) {
            for (int i = 0; i < LENGTH; i++) {
                file.write(String.valueOf(rand.nextInt(2)));
            }
            System.out.println("Сгенерировано " + LENGTH + " бит. Сохранено в " + outputPath);
        } catch (IOException e) {
            System.err.println("Ошибка записи в файл: " + e.getMessage());
            e.printStackTrace();
        }
    }

}
