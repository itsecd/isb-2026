import java.io.FileWriter;
import java.io.IOException;
import java.util.Random;

public class GenSequence {
    public static void main(String[] args) {
        int N = 128;
        Random rnd = new Random();
        try (FileWriter fw = new FileWriter("../../sequences/seq_java.txt")) {
            for (int i = 0; i < N; i++) {
                fw.write(rnd.nextInt(2) + "");
            }
        } catch (IOException e) {
            e.printStackTrace();
        }
    }
}
