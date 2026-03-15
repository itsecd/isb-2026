import java.io.FileWriter;
import java.io.IOException;
import java.security.SecureRandom;
import java.util.Random;

public class GenJava {
    public static String generateUtilRandom(int length) {
        Random random = new Random();
        StringBuilder sequence = new StringBuilder();
        
        for (int i = 0; i < length; i++) {
            sequence.append(random.nextInt(2));
        }
        
        return sequence.toString();
    }
    
    public static String generateSecureRandom(int length) {
        SecureRandom random = new SecureRandom();
        StringBuilder sequence = new StringBuilder();
        
        for (int i = 0; i < length; i++) {
            sequence.append(random.nextInt(2));
        }
        
        return sequence.toString();
    }
    
    public static String generateThreadLocalRandom(int length) {
        java.util.concurrent.ThreadLocalRandom random = java.util.concurrent.ThreadLocalRandom.current();
        StringBuilder sequence = new StringBuilder();
        
        for (int i = 0; i < length; i++) {
            sequence.append(random.nextInt(2));
        }
        
        return sequence.toString();
    }
    
    public static void main(String[] args) {
        int length = 128;
        
        String seq1 = generateUtilRandom(length);
        String seq2 = generateSecureRandom(length);
        String seq3 = generateThreadLocalRandom(length);
        
        try (FileWriter file = new FileWriter("sequences_java.txt")) {
            file.write("Sequence 1 (java.util.Random):\n" + seq1 + "\n\n");
            file.write("Sequence 2 (SecureRandom):\n" + seq2 + "\n\n");
            file.write("Sequence 3 (ThreadLocalRandom):\n" + seq3 + "\n");
        } catch (IOException e) {
            e.printStackTrace();
        }
        
        System.out.println("Sequences generated and saved to sequences_java.txt");
        System.out.println("Sequence 1: " + seq1);
        System.out.println("Sequence 2: " + seq2);
        System.out.println("Sequence 3: " + seq3);
    }
}