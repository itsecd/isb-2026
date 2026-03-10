import java.util.Random;
import java.io.FileWriter;

public class Gen_java {
    public static void main(String[] args) throws java.io.IOException {

        String bits = "";

        Random rand = new Random();
        for (int i = 0; i < 128; i++) {
            bits += rand.nextInt(2);
        }

        FileWriter f = new FileWriter("java.txt");
        f.write(bits);
        f.close();
    }
}