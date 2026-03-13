import java.util.Random;

public class Main {
    public static void main(String[] args) {
        Random rand = new Random();
        StringBuilder sequence = new StringBuilder();
        for (int i = 0; i < 128; i++) {
            sequence.append(rand.nextBoolean() ? "1" : "0");
        }
        System.out.println(sequence.toString());
    }
}