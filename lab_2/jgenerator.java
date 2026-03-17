import java.util.Random;
import java.io.FileWriter;
import java.io.IOException;

public class SimpleGenerator {
    public static void main(String[] args) {
        Random rand = new Random();
        StringBuilder seq = new StringBuilder();
        
        for(int i = 0; i < 128; i++) {
            char bit = (char)(rand.nextInt(2) + '0');
            seq.append(bit);
            System.out.print(bit);
        }
        System.out.println();
        
        try {
            FileWriter file = new FileWriter("sequence_java.txt");
            file.write(seq.toString());
            file.close();
        } catch(IOException e) {
            System.out.println("Ошибка записи");
        }
    }
}