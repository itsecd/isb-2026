import java.util.Random;

public class Generator {

    public static void main(String[] args) {

        Random rand = new Random();

        for (int i = 0; i < 128; i++) {
            System.out.print(rand.nextInt(2));
        }

        System.out.println();
    }
}