import java.util.*;
import java.io.*;

public class JavaGenerator {
    private static final int VECTOR_SIZE = 1000;
    private static final String OUTPUT_FILE = "JavaGenerated.txt";

    // Генерирует один случайный бит (0 или 1)
    public static int generateRandomBit() {
        return Math.random() >= 0.5 ? 1 : 0;
    }

    // Генерирует вектор из VECTOR_SIZE случайных битов
    public static List<Integer> generateRandomVector() {
        List<Integer> vector = new ArrayList<>();
        for (int i = 0; i < VECTOR_SIZE; i++) {
            vector.add(generateRandomBit());
        }
        return vector;
    }

    // Форматирует вектор в строку без разделителей
    private static String formatVector(List<Integer> vector) {
        StringBuilder sb = new StringBuilder();
        for (Integer bit : vector) {
            sb.append(bit);
        }
        return sb.toString();
    }

    public static void main(String[] args) {
        try (BufferedWriter writer = new BufferedWriter(new FileWriter(OUTPUT_FILE))) {
            for (int i = 0; i < VECTOR_SIZE; i++) {
                List<Integer> randomVector = generateRandomVector();
                String formatted = formatVector(randomVector);
                writer.write(formatted);
                writer.newLine(); // Перенос строки
            }
            System.out.println("Успешно записано " + VECTOR_SIZE + " строк в файл " + OUTPUT_FILE);
        } catch (IOException e) {
            System.err.println("Ошибка при записи в файл: " + e.getMessage());
            e.printStackTrace();
        }
    }
}
