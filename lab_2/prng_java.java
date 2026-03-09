import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.Random;

public class prng_java {
    public static void main(String[] args) {
        Random random = new Random();
        StringBuilder bits = new StringBuilder(128);

        // Генерируем последовательность из 128 бит (0 или 1)
        for (int i = 0; i < 128; i++) {
            bits.append(random.nextInt(2));
        }

        // Записываем результат в файл
        try {
            Files.writeString(Path.of("java_string.txt"), bits.toString());
            System.out.println("Успешно: 128 бит записаны в java_string.txt");
        } catch (IOException e) {
            System.err.println("Ошибка записи в файл: " + e.getMessage());
        }
    }
}