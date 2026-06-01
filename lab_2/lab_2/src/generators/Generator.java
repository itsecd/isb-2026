// lab_2/src/generators/Generator.java
// Генератор псевдослучайной последовательности на Java
// Использует java.util.Random

import java.io.FileWriter;
import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.util.Random;

public class Generator {
    
    private static final int SEQUENCE_LENGTH = 128;
    
    public static void main(String[] args) {
        try {
            String sequence = generateBinarySequence(SEQUENCE_LENGTH);
            
            // ✅ ОТНОСИТЕЛЬНЫЙ ПУТЬ через Path
            Path outputPath = Paths.get("../../data/sequences/java_sequence.txt")
                                   .normalize()
                                   .toAbsolutePath();
            Files.createDirectories(outputPath.getParent());
            
            saveToFile(sequence, outputPath.toString());
            
            System.out.println("[Java] Generated: " + sequence);
            System.out.println("[Java] Saved: " + outputPath);
            
        } catch (IOException e) {
            System.err.println("[Java] Error: " + e.getMessage());
            System.exit(1);
        }
    }
    
    /**
     * Генерирует бинарную последовательность заданной длины
     */
    private static String generateBinarySequence(int length) {
        Random random = new Random(System.currentTimeMillis());
        StringBuilder sb = new StringBuilder(length);
        
        for (int i = 0; i < length; i++) {
            sb.append(random.nextInt(2));
        }
        return sb.toString();
    }
    
    /**
     * Сохраняет данные в файл
     */
    private static void saveToFile(String data, String filepath) throws IOException {
        try (FileWriter writer = new FileWriter(filepath)) {
            writer.write(data);
        }
    }
}