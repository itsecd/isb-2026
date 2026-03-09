import java.io.FileWriter;
import java.io.IOException;
import java.util.Random;

public class pserand {
    private static final int N = 128;
    private static final long SEED = 11342;
    private static final String OUTPUT_FILENAME = "seq_java.txt";

    public static void main(String[] args) {
        Random random = new Random(SEED);
        try {
            FileWriter writer = new FileWriter(OUTPUT_FILENAME);
            for (int i = 0; i < N; i++) {
                int bit = random.nextInt(2); 
                writer.write(String.valueOf(bit));
            }
            writer.close();
        } catch (IOException e) {
            System.err.println("Ошибка ввода/вывода при записи файла: " + e.getMessage());
        }
    }
}