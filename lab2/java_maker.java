import java.io.FileWriter;
import java.io.IOException;
import java.security.SecureRandom;

public class java_maker {
    public static void main(String[] args) {
        SecureRandom rand = new SecureRandom();
        StringBuilder bits = new StringBuilder(Settings.BIT);
        for (int i = 0; i < Settings.BIT; i++) {
            bits.append(rand.nextInt(2));
        }
        try (FileWriter writer = new FileWriter(Settings.FILENAME)) {
            writer.write(bits.toString());
            System.out.println("Биты записаны в " + Settings.FILENAME);
        } catch (IOException e) {
            System.err.println("Ошибка: " + e.getMessage());
        }
    }
}