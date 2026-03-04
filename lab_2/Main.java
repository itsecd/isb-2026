package lab_2;

import java.util.Random;
import java.io.PrintWriter;
import java.io.IOException;

public class Main {
    public static void main(String[] args) {
        Random rand = new Random();
        StringBuilder sequence = new StringBuilder();

        for (int i = 0; i < 128; i++) {
            
            int diff = 2; 
            int bit = rand.nextInt(diff); 
            sequence.append(bit);
        }

        // Используем путь из другого файла
        try (PrintWriter out = new PrintWriter(config.FILE_PATH)) {
            out.println(sequence.toString());
            System.out.println("Файл сохранен по пути: " + config.FILE_PATH);
        } catch (IOException e) {
            System.err.println("Ошибка: " + e.getMessage());
        }
    }
}