package generator;
import java.util.Random;
import java.io.FileWriter;
import java.io.PrintWriter;
import java.io.IOException;

public class generator_Java {
    public static void main(String[] args) throws IOException {
        Random random = new Random();
        PrintWriter writer = new PrintWriter(new FileWriter("generator/java.txt"));

        for (int i = 0; i < 128; i++) {
            writer.print(random.nextInt(2));
        }

        writer.close();
        System.out.println("Java: java.txt");
    }
}