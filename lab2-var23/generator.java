// Генератор случайной битовой последовательности на Java
// Создаёт 128-битную последовательность с фиксированным seed и сохраняет в файл

import java.io.FileWriter;
import java.io.PrintWriter;
import java.util.Random;

public class generator {
    public static void main(String[] args) {
        // Создаём генератор случайных чисел с фиксированным seed
        Random rng = new Random(24);
        StringBuilder bitStream = new StringBuilder();

        // Генерируем 128 случайных битов (0 или 1)
        for (int index = 0; index < 128; index++) {
            bitStream.append(rng.nextInt(2));
        }

        // Записываем последовательность в файл с обработкой исключений
        try (PrintWriter writer = new PrintWriter(new FileWriter("gen_java.txt"))) {
            writer.print(bitStream);
            System.out.println("Последовательность успешно записана в gen_java.txt");
        } catch (Exception ex) {
            System.out.println("Ошибка при работе с файлом: " + ex.getMessage());
        }
    }
}