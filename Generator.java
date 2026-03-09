import java.io.*;
import java.util.Random;

public class Generator {
    public static void main(String[] args) throws IOException {
        Random rng = new Random(42);
        PrintWriter out = new PrintWriter(new FileWriter("java_seq.txt"));
        
        for (int i = 0; i < 128; i++) {
            out.print(rng.nextInt(2));
        }
        
        out.close();
    }
}