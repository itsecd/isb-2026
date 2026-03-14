import java.util.Random;
import java.io.PrintWriter;
import java.io.FileWriter;
import java.io.IOException;

public class Generator {
    public static void main(String[] args) {
        long seed = 12345L;
        Random rand = new Random(seed);

        int N = 128;

        PrintWriter out = new PrintWriter(System.out, true);
        if (args.length > 0) {
            try {
                out = new PrintWriter(new FileWriter(args[0]));
            } catch (IOException e) {
                System.err.println("Ошибка при создании файла: " + e.getMessage());
                System.exit(1);
            }
        }

        for (int i = 0; i < N; i++) {
            out.print(rand.nextInt(2));
        }
        out.println();

        if (out != null && args.length > 0) {
            out.close();
        }
    }
}