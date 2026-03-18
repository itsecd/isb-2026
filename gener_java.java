import java.util.Random;
import java.io.FileWriter;
import java.io.IOException;

public class gener_java {
    public static void generateAndPrint(int length, String filename) {
        Random rand = new Random();
        StringBuilder sb = new StringBuilder();
        
        for (int i = 0; i < length; i++) {
            int bit = rand.nextInt(2);
            System.out.print(bit);
            sb.append(bit);
        }
        
        try (FileWriter writer = new FileWriter(filename)) {
            writer.write(sb.toString());
        } catch (IOException e) {
            System.out.println("Ошибка записи файла: " + e.getMessage());
        }
    }
    
    public static void main(String[] args) {
        generateAndPrint(128, "seq_java.txt");
        System.out.println();
    }
}
