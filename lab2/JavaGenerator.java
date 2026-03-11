import java.io.FileWriter;
import java.io.IOException;
import java.util.Random;

public class JavaGenerator {
    public static void main(String[] args) {
        Random rand = new Random();
        StringBuilder sequence = new StringBuilder();
        
        for (int i = 0; i < 128; i++) {
            sequence.append(rand.nextInt(2));
        }
        
        String result = sequence.toString();
        
        System.out.println("Java последовательность (128 бит):");
        System.out.println(result);
        
        try (FileWriter writer = new FileWriter("sequence_java.txt")) {
            writer.write(result);
            System.out.println("Сохранено в sequence_java.txt");
        } catch (IOException e) {
            System.out.println("Ошибка при сохранении файла");
            e.printStackTrace();
        }
    }
}