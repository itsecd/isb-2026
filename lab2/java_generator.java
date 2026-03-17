import java.util.Random;
import java.io.FileWriter;
import java.io.IOException;

public class Main {
    public static void main(String[] args) {
        Random rand = new Random();
        StringBuilder res = new StringBuilder(128);
        
        for (int i = 0; i < 128; i++) {
            res.append(rand.nextInt(2));
        }
        
        try (FileWriter f = new FileWriter("Java.txt")) {
            f.write(res.toString());
        } catch (IOException e) {
            e.printStackTrace();
        }
    }
}
