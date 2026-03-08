import java.io.FileWriter;
import java.io.IOException;
import java.util.ArrayList;
import java.util.Random;

public class generator_j {
    public static void main(String[] args) {
        generator("output_java.txt");
    }
    public static void write_data(ArrayList<String> data,String filenameoutput){
        try (FileWriter writer = new FileWriter(filenameoutput)) {
            for (String item : data) {
                writer.write(item);
            }
        } catch (IOException e) {
            e.printStackTrace();
        }
    }
    public static void generator(String filenameoutput){
        ArrayList<String> data = new ArrayList<String>();
        Random random = new Random();
        for(int i=0;i<128;i++){
            data.add(Integer.toString(random.nextInt(2)));
        }
        write_data(data,filenameoutput);
    }
}
