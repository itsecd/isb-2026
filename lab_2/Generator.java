import java.util.Random;

public class Generator {
    public static void main(String[] args) {
        Random rand = new Random();
        // Инициализация seed на основе времени по умолчанию

        int numBits = 128;
        StringBuilder binarySequence = new StringBuilder();

        System.out.println("Сгенерированная последовательность (Java):");
        for (int i = 0; i < numBits; i++) {
            // Генерируем случайный бит
            char bit = rand.nextBoolean() ? '1' : '0';
            binarySequence.append(bit);
            System.out.print(bit);
            if ((i + 1) % 8 == 0) System.out.print(' ');
        }
        System.out.println();
    }
}