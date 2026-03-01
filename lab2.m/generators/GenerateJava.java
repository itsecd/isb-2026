import java.io.FileWriter;
import java.util.Random;

public class GenerateJava {
    public static void main(String[] args) {
        Random rand = new Random();
        String sequence = "";
        
        for (int i = 0; i < 128; i++) {
            sequence += rand.nextInt(2);
        }
        
        try {
            FileWriter writer = new FileWriter("../sequences/sequence_java.txt");
            writer.write(sequence);
            writer.close();
            System.out.println("Сохранено в ../sequences/sequence_java.txt");
        } catch (Exception e) {
            System.out.println("Ошибка: " + e.getMessage());
        }
    }
}