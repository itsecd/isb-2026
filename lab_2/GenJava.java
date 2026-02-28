import java.io.FileWriter;
import java.io.IOException;
import java.util.Random;

public class GenJava {
    public static void main(String[] args) throws IOException {
        long seed = 12345L;
        int N = 128;

        Random rng = new Random(seed);
        StringBuilder sb = new StringBuilder(N);

        for (int i = 0; i < N; i++) {
            sb.append(rng.nextBoolean() ? '1' : '0');
        }

        try (FileWriter fw = new FileWriter("seq_java.txt")) {
            fw.write(sb.toString());
            fw.write("\n");
        }

        System.out.println("Saved 128-bit sequence to seq_java.txt");
    }
}