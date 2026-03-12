import java.util.Random;
import java.io.FileWriter;
import java.io.IOException;

public class RandomGenerator {
    public static void main(String[] args) {
        // Генератор на основе вихря Мерсенна (аналог mt19937)
        Random gen = new Random();
        
        StringBuilder sequence = new StringBuilder();
        
        System.out.println("Сгенерированная последовательность (Java):");
        for (int i = 0; i < 128; i++) {
            int bit = gen.nextInt(2); // 0 или 1
            sequence.append(bit);
            System.out.print(bit);
        }
        System.out.println();
        
        // Сохранение в файл
        try {
            FileWriter writer = new FileWriter("sequence_java.txt");
            writer.write(sequence.toString());
            writer.close();
            System.out.println("\nПоследовательность сохранена в файл: sequence_java.txt");
        } catch (IOException e) {
            System.out.println("Ошибка при создании файла: " + e.getMessage());
        }
    }
}