import java.util.Random;
import java.io.FileWriter;
import java.io.IOException;

public class generator {
    public static void main(String[] args) throws IOException {

        Random rand = new Random();
        FileWriter file = new FileWriter("../sequences/seq_java.txt");

        for (int i = 0; i < 128; i++) {
            int bit = rand.nextInt(2);
            System.out.print(bit);
            file.write(Integer.toString(bit));
        }

        file.close();
    }
}