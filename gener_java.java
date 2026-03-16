import java.util.Random;

public class gener_java {
    public static void generateAndPrint(int length) {
        Random rand = new Random();
        
        for (int i = 0; i < length; i++) {
            int bit = rand.nextInt(2);
            System.out.print(bit);
        }
    }
    
    public static void main(String[] args) {
        generateAndPrint(128);
        System.out.println();
    }
}