import java.io.FileWriter;
import java.io.IOException;
import java.util.Random;

public class Gen {

    public static void main(String[] args) {

        try {
            Random rnd = new Random();

            FileWriter writer = new FileWriter("java_sequence.txt");

            for (int i = 0; i < 128; i++) {
                writer.write(String.valueOf(rnd.nextInt(2)));
            }

            writer.close();

            System.out.println("Java: файл успешно создан");

        } catch (IOException e) {
            System.out.println("Ошибка Java генерации: " + e.getMessage());
        }
    }
}