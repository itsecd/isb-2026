import java.util.Random;
import java.io.FileWriter;
import java.io.IOException;
import java.io.PrintWriter;

public class Main {
    public static void main(String[] args) throws IOException {
        Random random = new Random();
        PrintWriter writer = new PrintWriter(new FileWriter("seq_j.txt"));
        
        for (int i = 0; i < 128; i++) {
            writer.print(random.nextInt(2));
        }
        
        writer.close();
    }
}