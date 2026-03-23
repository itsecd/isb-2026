import java.util.Random;
import java.io.PrintWriter;

public class Generator {
    public static void main(String[] args) throws Exception {
        Random rand = new Random();
        PrintWriter out = new PrintWriter("sequence_java.txt");
        for (int i = 0; i < 128; i++) {
            out.print(rand.nextInt(2));
        }
        out.println();
        out.close();
    }
}