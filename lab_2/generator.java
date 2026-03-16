import java.io.FileWriter;
import java.io.IOException;
import java.util.Random;

public class GenJava {
    public static void main(String[] args) throws IOException {
        Random rand = new Random();
        FileWriter file = new FileWriter("seq_java.txt");

        for(int i = 0; i < 128; i++) {
            int bit = rand.nextInt(2);
            System.out.print(bit);
            file.write(String.valueOf(bit));
        }
        
        file.close();
    }
}