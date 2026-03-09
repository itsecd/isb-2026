import java.io.IOException;
import java.nio.file.*;
import java.util.Random;

public class Main {
    public static void main(String[] args) {
        Random random = new Random(42);
        byte[] r_bytes = new byte[16]; // 128 бит = 16 байт
        random.nextBytes(r_bytes);

        String binary_string = "";
        for (byte b: r_bytes) { // Представление байтов в виде бинарных строк
            binary_string += String.format("%8s", Integer.toBinaryString(b & 0xFF)).replace(' ', '0');
        }
        System.out.println(binary_string);

        Path output = Paths.get("output_java.txt");
        try {
            Files.writeString(output, binary_string);
        } catch (IOException e) {
            System.out.println("Ошибка при работе с файлом!");
            e.printStackTrace();
        }
    }
}