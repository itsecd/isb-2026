import java.io.FileWriter;
import java.io.IOException;
import java.util.Random;

public class rng {

    public static void main(String[] args) {
        try {
            
        String bits = "";
        
        Random r= new Random();
        for(int i = 0; i<128; i++)
        {
        bits += r.nextInt(2);
        }
        
        System.out.println(bits);
        
        FileWriter Writer = new FileWriter("java_random_vec.txt", false);
        Writer.write(bits);
        Writer.close();
        
        }
        catch(IOException ex){
            System.out.println(ex.getMessage());
        }
    }
}