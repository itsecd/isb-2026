import java.io.FileWriter;
import java.io.IOException;
import java.util.Random;

public class generator {
    
    public static void main(String[] args) {
        generator("output.txt");
    }
    
    public static void write_file(String filename, String data) {
        try {
            FileWriter writer = new FileWriter(filename);
            writer.write(data);
            writer.close();
        } catch (IOException e) {
            e.printStackTrace();
        }
    }
    
    public static void generator(String filename) {
        long seed = System.currentTimeMillis();
        Random rand = new Random(seed);
        StringBuilder sb = new StringBuilder();
        for (int i = 0; i < 128; i++) {
            int num = rand.nextInt(2);
            sb.append(num);
        }
        write_file(filename, sb.toString()); 
    }
}