import java.util.Random;
import java.io.FileWriter;
import java.io.IOException;


public class random_gen{
    public static void main(String[] args) {
        generator("java_gen.txt");
    }
    public static void generator(String path){
        StringBuilder data = new StringBuilder();
        Random num = new Random();
        for (int i = 0; i < 128; i++) {
            data.append(num.nextInt(2));
        }
        save_data(data.toString(), path);
    }
    public static void save_data(String data, String path){
        try {
            FileWriter writer = new FileWriter(path);
            writer.write(data);
            writer.close();
        } catch (IOException e) {
            e.printStackTrace();
        }

    }
}