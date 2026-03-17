import java.io.FileWriter;
import java.io.IOException;
import java.util.Random;

public class RandomSequenceGenerator {
    
    public static boolean[] generateRandomBits() {
        Random random = new Random();
        boolean[] bits = new boolean[128];
        
        for (int i = 0; i < 128; i++) {
            bits[i] = random.nextBoolean();
        }
        
        return bits;
    }
    
    public static void saveToFile(boolean[] bits, String filename) {
        try (FileWriter writer = new FileWriter(filename)) {
            for (boolean bit : bits) {
                writer.write(bit ? '1' : '0');
            }
        } catch (IOException e) {
            e.printStackTrace();
        }
    }
    

    public static void main(String[] args) {
        
        boolean[] seq1 = generateRandomBits();
        saveToFile(seq1, "java_sequence_1.txt");
        
    }
}