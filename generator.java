import java.io.FileWriter;
import java.io.IOException;
import java.io.PrintWriter;
import java.util.Random;

public class generator {
    public static void main(String[] args) {
        Random random = new Random(42);
        
        int bitsNeeded = 128;
        StringBuilder binarySequence = new StringBuilder();
        
        for (int i = 0; i < bitsNeeded; i++) {
            // nextInt(2) дает 0 или 1
            int bit = random.nextInt(2);
            binarySequence.append(bit);
        }

        System.out.println("Сгенерированная последовательность (Java):");
        System.out.println(binarySequence.toString());
        
        try (PrintWriter out = new PrintWriter(new FileWriter("seq_java.txt"))) {
            out.print(binarySequence.toString());
            System.out.println("Последовательность сохранена в файл seq_java.txt");
        } catch (IOException e) {
            System.err.println("Ошибка записи в файл: " + e.getMessage());
        }
    }
}