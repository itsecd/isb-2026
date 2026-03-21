import java.io.FileWriter;
import java.io.IOException;
import java.security.SecureRandom;
import java.util.logging.Level;
import java.util.logging.Logger;

public class Main {
    private static final Logger logger = Logger.getLogger(Main.class.getName());

    public static void main(String[] args) {
        String file = "java_random.txt";

        try (FileWriter writer = new FileWriter(file)) {

            SecureRandom secureRandom = new SecureRandom();

            for (int i = 0; i < 128; ++i) {
                writer.write(String.valueOf(secureRandom.nextInt(2)));
            }

            logger.info("Sequence was generated and wrote in " + file);
        } catch (IOException e) {
            logger.log(Level.SEVERE, "Cant open txt to write in random sequence.", e);
        }
    }
}
