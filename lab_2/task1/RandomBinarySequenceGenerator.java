import java.util.Random;
import java.io.FileWriter;
import java.io.IOException;
import java.io.PrintWriter;
import java.io.File;
import java.util.Scanner;

public class RandomBinarySequenceGenerator {
    
    public static void main(String[] args) {
        System.out.println("Генерация псевдослучайных бинарных последовательностей длиной 128 бит");
        System.out.println("====================================================================");
        
        // Создаем генератор случайных чисел
        String randomSeq1 = generateWithRandom();
        
        // Выводим на экран с пробелами для читаемости
        printBinarySequence(randomSeq1);
        
        // Спрашиваем пользователя, куда сохранить файл
        saveSequenceWithUserInput(randomSeq1);
    }

    public static String generateWithRandom() {
        Random random = new Random();
        StringBuilder binaryString = new StringBuilder(128);
        
        for (int i = 0; i < 128; i++) {
            int bit = random.nextInt(2);
            binaryString.append(bit);
        }
        
        return binaryString.toString();
    }
    
    public static void saveSequenceWithUserInput(String sequence) {
        Scanner scanner = new Scanner(System.in);
        
        System.out.println("\n--- Сохранение файла ---");
        System.out.println("Введите полный путь для сохранения файла (включая имя файла):");
        System.out.println("Например: C:\\Programming\\University\\2nd_course\\Inf_sec_basics\\Release\\lab2\\task2\\sequence_java.txt");
       
        String filePath = scanner.nextLine().trim();
        
        if (filePath.isEmpty()) {
            filePath = "binary_sequence.txt";
            System.out.println("Используется имя по умолчанию: " + filePath);
        }
        
        
        File file = new File(filePath);
        File parentDir = file.getParentFile();
        
        
        if (parentDir != null && !parentDir.exists()) {
            System.out.println("Указанная директория не существует: " + parentDir);
            System.out.println("Хотите создать её? (да/нет)");
            String answer = scanner.nextLine().trim().toLowerCase();
            
            if (answer.equals("да") || answer.equals("yes") || answer.equals("y")) {
                if (parentDir.mkdirs()) {
                    System.out.println("Директория создана: " + parentDir);
                } else {
                    System.out.println("Не удалось создать директорию!");
                    System.out.println("Файл будет сохранен в текущую директорию.");
                    filePath = "binary_sequence.txt";
                }
            } else {
                System.out.println("Файл будет сохранен в текущую директорию.");
                filePath = "binary_sequence.txt";
            }
        }
        
        saveSequenceToFile(sequence, filePath);
        
        scanner.close();
    }
    
    public static void saveSequenceToFile(String sequence, String filename) {
        try (PrintWriter writer = new PrintWriter(new FileWriter(filename))) {
            writer.print(sequence);
            
            System.out.println("\n✓ Файл успешно сохранен!");
            System.out.println("  Путь: " + new File(filename).getAbsolutePath());
            System.out.println("  Размер: " + sequence.length() + " байт");
            
        } catch (IOException e) {
            System.err.println("\n✗ ОШИБКА при сохранении в файл: " + e.getMessage());
            System.err.println("  Проверьте, что у вас есть права на запись в эту директорию.");
        }
    }
    
    public static void printBinarySequence(String sequence) {
        if (sequence.length() != 128) {
            System.out.println("Ошибка: длина последовательности не равна 128 бит");
            return;
        }
        
        System.out.println("\nСгенерированная последовательность:");
        for (int i = 0; i < 128; i += 8) {
            String byteStr = sequence.substring(i, Math.min(i + 8, 128));
            System.out.print(byteStr);
            if (i < 120) {
                System.out.print(" ");
            }
        }
        System.out.println();
    }
}