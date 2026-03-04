import java.util.Random;
import java.io.FileWriter;
import java.io.IOException;
import java.io.File;


public class java_generator {
    public static void main(String[] args) {
        // Использую java.util.Random
        Random rand = new Random();
        StringBuilder sequence = new StringBuilder();
        
        // Генерируем 128 бит
        for (int i = 0; i < 128; i++) {
            sequence.append(rand.nextInt(2));
        }
        
        String seq_str = sequence.toString();
        
        System.out.println("JAVA ГЕНЕРАТОР ПСЕВДОСЛУЧАЙНОЙ ПОСЛЕДОВАТЕЛЬНОСТИ");
        System.out.println("Генератор: java.util.Random (linear congruential)");
        System.out.println("Длина: 128 бит");
        System.out.println("Последовательность:");
        System.out.println(seq_str);
        
        // Создаю папку sequences, если её нет
        File directory = new File("sequences");
        if (!directory.exists()) {
            directory.mkdirs();
        }
        
        try {
            FileWriter writer = new FileWriter("sequence_java.txt");
            writer.write(seq_str);
            writer.close();
            System.out.println("Последовательность сохранена в файл: sequence_java.txt");
        } catch (IOException e) {
            System.out.println("Ошибка при сохранении в файл: " + e.getMessage());
        }
    }
}