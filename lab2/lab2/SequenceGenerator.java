import java.io.FileWriter;
import java.io.IOException;
import java.util.Random;

public class SequenceGenerator {
    
    public static void generateRandomSequence(String path) {        
        int length = 128;
        
        Random random = new Random();
        StringBuilder seq = new StringBuilder(length);
        
        for (int i = 0; i < length; i++) {
            seq.append(random.nextInt(2));
        }
        
                try (FileWriter fileWriter = new FileWriter(path)) {
            fileWriter.write(seq.toString());
        } catch (IOException e) {
            e.printStackTrace();
        }
    }
	
	public static void main(String[] args) {
        generateRandomSequence("java_sequence.txt");
    }
}