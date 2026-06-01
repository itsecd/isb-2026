import java.io.FileWriter;
import java.io.IOException;
import java.util.Random;

public class RandomBitsGenerator {
    public static void main(String[] args) {
        Random random = new Random();
        StringBuilder bits = new StringBuilder();
        
        for (int i = 0; i < 128; i++) {
            bits.append(random.nextInt(2)); 
        }
        
        try (FileWriter writer = new FileWriter("result_java.txt")) {
            writer.write(bits.toString());
        } catch (IOException e) {
            e.printStackTrace();
        }
    }
}