import java.io.FileWriter;
import java.io.IOException;
import java.io.PrintWriter;
import java.util.Random;

public class generator_java {
    public static void main(String[] args) throws IOException {  // throws добавлен
        Random random = new Random();
        
        try (PrintWriter writer = new PrintWriter(new FileWriter("seq_java.txt"))) {
            for (int i = 0; i < 128; i++) {
                writer.print(random.nextInt(2));
            }
        }
    }
}