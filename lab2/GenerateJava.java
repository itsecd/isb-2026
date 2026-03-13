import java.util.Random;

public class GenerateJava {
    public static void main(String[] args) {
        Random rand = new Random();
        System.out.println("Java Generated Sequence (128 bits):");
        for (int i = 0; i < 128; i++) {
            System.out.print(rand.nextBoolean() ? "1" : "0");
        }
        System.out.println();
    }
}
