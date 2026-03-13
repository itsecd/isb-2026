import java.io.FileWriter;
import java.io.IOException;
import java.security.SecureRandom;
import java.util.Random;

public class Generator {
    public static String generateSequenceRandom(int length) {
        Random random = new Random();
        StringBuilder sequence = new StringBuilder();
        
        for (int i = 0; i < length; i++) {
            sequence.append(random.nextInt(2));
        }
        return sequence.toString();
    }
    public static String generateSequenceSecure(int length) {
        SecureRandom secureRandom = new SecureRandom();
        StringBuilder sequence = new StringBuilder();
        
        for (int i = 0; i < length; i++) {
            sequence.append(secureRandom.nextInt(2));
        }
        return sequence.toString();
    }
    
    public static String generateSequenceLCG(int length) {
        long seed = System.currentTimeMillis();
        StringBuilder sequence = new StringBuilder();
        
        for (int i = 0; i < length; i++) {
            seed = (seed * 1103515245 + 12345) & 0x7fffffff;
            sequence.append(seed % 2);
        }
        return sequence.toString();
    }
    
    public static void main(String[] args) {
        int LENGTH = 128;
        
        String seq1 = generateSequenceLCG(LENGTH);
        String seq2 = generateSequenceRandom(LENGTH);
        String seq3 = generateSequenceSecure(LENGTH);
        
        try {
            FileWriter file = new FileWriter("sequences_java.txt");
            file.write("Sequence 1 (LCG): " + seq1 + "\n");
            file.write("Sequence 2 (Random): " + seq2 + "\n");
            file.write("Sequence 3 (SecureRandom): " + seq3 + "\n");
            file.close();
            
            System.out.println("Generated sequences saved to sequences_java.txt");
            System.out.println("Sequence 1: " + seq1);
            System.out.println("Sequence 2: " + seq2);
            System.out.println("Sequence 3: " + seq3);
        } catch (IOException e) {
            e.printStackTrace();
        }
    }
}