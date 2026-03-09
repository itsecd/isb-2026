import java.io.FileWriter;
import java.io.IOException;
import java.util.Random;

public class posled3 {
    public static void main(String[] args) {
        try {
            Random random = new Random();
            StringBuilder bits = new StringBuilder();
            
            for (int i = 0; i < 128; i++) {
                bits.append(random.nextInt(2));
            }
            
            try (FileWriter writer = new FileWriter("java_posled.txt")) {
                writer.write(bits.toString());
                System.out.println("Java sequence (128 bit):");
                for (int i = 0; i < bits.length(); i++) {
                    System.out.print(bits.charAt(i));
                    if ((i + 1) % 8 == 0 && i != bits.length() - 1) System.out.print(" ");
                }
                System.out.println();
                System.out.println("save in java_posled.txt");
            } catch (IOException e) {
                System.err.println("Error when writing to a file: " + e.getMessage());
                throw e;
            }
        } catch (Exception e) {
            System.err.println("Unexpected error: " + e.getMessage());
            e.printStackTrace();
        }
    }
}