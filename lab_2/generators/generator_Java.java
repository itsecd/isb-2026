import java.util.Random;
import java.io.FileWriter;

public class main {
    public static void main(String[] args) {

        String res = "";

        Random rand = new Random();
        for (int i = 0; i < 128; i++) {
            res += rand.nextInt(2);
        }

        FileWriter f = new FileWriter("Java.txt");
        f.write(res);
        f.close();
    }
}