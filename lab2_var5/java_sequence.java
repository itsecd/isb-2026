import java.util.Random;
import java.io.FileWriter;
import java.io.IOException;

public class java_sequence {
    public static void main(String[] args) {
        StringBuilder res = new StringBuilder();
        Random rand = new Random();
    
        for (int i = 0; i < 128; i++) {
            res.append(rand.nextInt(2));
        }
      
        try (FileWriter f = new FileWriter("java_sequence.txt")) {
            f.write(res.toString());
            System.out.println("Файл создан.");
        } catch (IOException e) {
            System.out.println("Ошибка при записи в файл: " + e.getMessage());
        }
    }
}