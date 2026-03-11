import java.io.FileWriter;
import java.util.Random;

public class Generator {
    public static void main(String[] args) throws Exception {

        Random rand = new Random();
        FileWriter file = new FileWriter("bits_java.txt");

        for(int i = 0; i < 128; i++){
            file.write(Integer.toString(rand.nextInt(2)));
        }

        file.close();
    }
}