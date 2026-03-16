import java.util.Random;

public class Main {
    public static void main(String[] args) {
        Random random = new Random();
        
        for (int i = 0; i < 128; i++) {
            System.out.print(random.nextInt(2));
        }
        System.out.println();
    }
}