import java.util.Random;
import java.io.FileWriter;

public class JavaGenerator {
    public static void main(String[] args) throws Exception {
        Random rand = new Random();
        FileWriter fw = new FileWriter("java_sequence.txt");
        
        for (int i = 0; i < 128; i++) {
            fw.write(String.valueOf(rand.nextInt(2)));
        }
        
        fw.close();
        System.out.println("Generated java_sequence.txt");
    }
}