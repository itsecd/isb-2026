import java.io.FileWriter;
import java.io.PrintWriter;
import java.util.Random;

public class generator {
    public static void main(String[] args) {
        Random random = new Random(42);
        StringBuilder binarySequence = new StringBuilder();
        
        for (int i = 0; i < 128; i++) {
            binarySequence.append(random.nextInt(2));
        }

        try (PrintWriter out = new PrintWriter(new FileWriter("seq_java.txt"))) {
            out.print(binarySequence.toString());
            System.out.println("Последовательность сохранена в seq_java.txt");
        } catch (Exception e) {
            System.out.println("Ошибка: " + e.getMessage());
        }
    }
}