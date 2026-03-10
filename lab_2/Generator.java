import java.io.FileWriter;
import java.util.Random;

public class Generator{
    public static void main(String[] args) {
        int N = 128;
        String seq = "";
        Random random = new Random();

        for(int i = 0; i < N; i++){
            int bit = random.nextInt(2);
            seq = seq + bit;
        }

        System.out.println("Generated sequence (java):");
        System.out.println(seq);

        try {
            FileWriter writer = new FileWriter("seq_java.txt");
            writer.write(seq);
            writer.close();
        } catch (IOException e) {
            System.out.println("Error");
        }
    }
}