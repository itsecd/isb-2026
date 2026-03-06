import java.util.Random;
import java.io.FileWriter;
import java.io.IOException;
import java.io.File;


public class java_generator {
    public static void main(String[] args) {
        // Использую java.util.Random
        Random rand = new Random();//Создаю объект класса Random для генерации случайных чисел
        StringBuilder sequence = new StringBuilder();//динамическое добавление символов
        
        // Генерируем 128 бит
        for (int i = 0; i < 128; i++) {
            sequence.append(rand.nextInt(2));//Генерирует случайное число от 0 до 1 (nextInt(2)) и добавляет его в конец StringBuilder
        }
        
        String seq_str = sequence.toString();//преобразует битовую последовательность а строку
        
        // Создаю папку sequences, если её нет
        File directory = new File("sequences");
        if (!directory.exists()) {
            directory.mkdirs();
        }
        
        try {
            FileWriter writer = new FileWriter("sequence_java.txt");//Создает объект FileWriter для записи в файл "sequence_java.txt"
            writer.write(seq_str);//Записываем сгенерированную последовательность в файл
            writer.close();
            System.out.println("Последовательность сохранена в файл: sequence_java.txt");
        } catch (IOException e) {
            System.out.println("Ошибка при сохранении в файл: " + e.getMessage());
        }
    }
}