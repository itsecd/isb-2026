import java.io.FileWriter;
import java.io.IOException;
import java.util.Random;

public class generate {
    public static void main(String[] args) {
        Random random = new Random();
        int bitsNeeded = 128;
        StringBuilder binarySequence = new StringBuilder();

        // Генерируем 128 бит. Integer.SIZE = 32 бита, значит нужно 4 итерации.
        int iterations = bitsNeeded / Integer.SIZE;

        for (int i = 0; i < iterations; i++) {
            int number = random.nextInt(); // Генерирует случайное 32-битное int
            // Преобразуем в бинарную строку, дополняя нулями слева до 32 знаков
            String binaryPart = String.format("%32s", Integer.toBinaryString(number)).replace(' ', '0');
            binarySequence.append(binaryPart);
        }

        String result = binarySequence.toString();

        try (FileWriter writer = new FileWriter("lab_2/sequence_java.txt")) {
            writer.write(result);
            System.out.println("Generated Comlite. Write in sequence_java.txt");
            System.out.println("Result: " + result);
        } catch (IOException e) {
            System.err.println("Error writling in file: " + e.getMessage());
        }
    }
}