import java.util.Random;


public class RandomGenerator {
    public static void generate_128() {
        Random rand = new Random();
        StringBuilder sequence = new StringBuilder();

        for (int i = 0; i < 128; ++i) {
            sequence.append(rand.nextInt(2));
        }

        System.out.println("generated seq:");
        System.out.println(sequence.toString());
    }

    public static void main(String[] args) {
        generate_128();
    }
}