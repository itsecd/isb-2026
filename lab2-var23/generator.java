import java.io.FileWriter;
import java.io.PrintWriter;
import java.util.Random;

public class generator {
    public static void main(String[] args) {
        Random rng = new Random(24);
        StringBuilder bitStream = new StringBuilder();

        for (int index = 0; index < 128; index++) {
            bitStream.append(rng.nextInt(2));
        }

        try (PrintWriter writer = new PrintWriter(new FileWriter("gen_java.txt"))) {
            writer.print(bitStream);
            System.out.println("Последовательность успешно записана в gen_java.txt");
        } catch (Exception ex) {
            System.out.println("Ошибка при работе с файлом: " + ex.getMessage());
        }
    }
}