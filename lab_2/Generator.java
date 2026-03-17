import java.util.Random;

public class generator {
    public static void main(String[] args) {
        Random rng = new Random(12345L);
        StringBuilder sb = new StringBuilder(128);
        for (int i = 0; i < 128; i++) {
            sb.append(rng.nextInt(2));
        }
        System.out.println(sb.toString());
    }
}