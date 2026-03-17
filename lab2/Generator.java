import java.io.FileWriter;
import java.io.IOException;
import java.util.Random;
import java.io.File;

public class Generator {
    
    private static void createDirectory(String dirName) {
        File directory = new File(dirName);
        if (!directory.exists()) {
            directory.mkdir();
        }
    }
    
    public static String generateBits(int length) {
        Random rand = new Random();
        StringBuilder bits = new StringBuilder();
        for (int i = 0; i < length; i++) {
            bits.append(rand.nextInt(2));
        }
        return bits.toString();
    }
    
    public static void main(String[] args) {
        createDirectory("sequences");
        
        String bits = generateBits(128);
        
        try (FileWriter file = new FileWriter("sequences/java_sequence.txt")) {
            file.write(bits);
            System.out.println("Java: sequences/java_sequence.txt (128 бит)");
        } catch (IOException e) {
            e.printStackTrace();
        }
    }
}