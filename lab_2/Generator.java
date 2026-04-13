import java.io.FileWriter;
import java.io.IOException;
import java.util.Random;

public class Generator {

    public static void main(String[] args) throws IOException {

        Random random = new Random();

        for (int j = 1; j <= 3; j++) {

            String filename = "sequence" + j + ".txt";
            FileWriter file = new FileWriter(filename);

            for (int i = 0; i < 128; i++) {
                int bit = random.nextInt(2);
                file.write(String.valueOf(bit));
            }

            file.close();
        }

        System.out.println("3 sequences generated and saved.");
    }
}