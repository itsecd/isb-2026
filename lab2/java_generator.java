package lab2;

import java.io.FileWriter;
import java.io.IOException;
import java.util.Random;


public class java_generator {
    //генерирует псевдослучайную последовательность из 128 бит
    public static String generateRandomSequence() {
        StringBuilder sequence = new StringBuilder();
        Random random = new Random();

        for (int i = 0; i < 128; i++) {
            int sequenceElement = random.nextInt(2);
            sequence.append(sequenceElement);
        }

        return sequence.toString();
    }


    ////записывает последовательность в файл
    public static void writeFile(String fileName, String sequence) {
        try (FileWriter writer = new FileWriter(fileName)) {
            writer.write(sequence);
        } catch (IOException e) {
            System.err.println("Error: " + e.getMessage());
        }
    }


    public static void main(String[] args) {
        String sequence = generateRandomSequence();
        writeFile("lab2/java_sequence.txt", sequence);
    }
}