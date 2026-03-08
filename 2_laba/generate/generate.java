import java.io.FileWriter;
import java.io.IOException;
import java.util.ArrayList;
import java.util.List;
import java.util.Random;

public class generate {
    public static List<Integer> generateBits(long seed, int n) {
        Random rand = new Random(seed);
        List<Integer> result = new ArrayList<>(n);

        while (result.size() < n) {
            int key = rand.nextInt();
            for (int i = 0; i < 32 && result.size() < n; i++)
                result.add((key >> i) & 1);
        }
        return result;
    }

    public static void writeToFile(String path, List<Integer> req) {
        try (FileWriter writer = new FileWriter(path)) {
            for (int elem : req)
                writer.write(elem == 0 ? '0' : '1');
        } catch (IOException e) {
            System.err.println("Ошибка записи в файл: " + e.getMessage());
        }
    }

    public static void main(String[] args) {
        int n = 128;
        long seed = 11342;

        List<Integer> bits = generateBits(seed, n);
        writeToFile("generate_java.txt", bits);
    }
}