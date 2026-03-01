import java.util.Random;

public class Main {
    public static void main(String[] args) {
        Random rand = new Random();
        StringBuilder sequence = new StringBuilder();

        for (int i = 0; i < 128; i++) {
            int bit = rand.nextInt(2); 
            sequence.append(bit);
        }

        System.out.println("Length: " + sequence.length());
        System.out.println(sequence.toString());
    }
}
