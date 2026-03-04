package generators;

import java.io.FileWriter;
import java.util.Random;

public class generator{
    public static void main(String[] args) throws Exception{
        Random r = new Random();
        StringBuilder sb = new StringBuilder();

        int bit_count = 128;
        String filename = "lab_2/gen_bits/java_gen.txt";

        if (args.length > 0) bit_count = Integer.parseInt(args[0]);
        if (args.length > 1) filename = args[1];


        for(int i = 0; i < bit_count; i++) sb.append(r.nextInt(2));
        new FileWriter(filename).append(sb).close();
    }
}