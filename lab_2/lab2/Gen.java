import java.util.Random;

public class Gen {
    public static void main(String[] args) {

        Random rand = new Random();
        int n = 128;

        StringBuilder bits = new StringBuilder();

        for (int i = 0; i < n; i++) {
            bits.append(rand.nextInt(2));
        }

        System.out.println(bits.toString());
    }
}