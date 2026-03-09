import java.io.*;
import java.util.*;

public class generate_java {
    static List<Double> readConstants() throws IOException {
        List<Double> values = new ArrayList<>();
        BufferedReader br = new BufferedReader(new FileReader("constants.txt"));
        String line;
        while ((line = br.readLine()) != null) {
            int comment = line.indexOf('#');
            if (comment != -1) line = line.substring(0, comment);
            line = line.trim();
            if (!line.isEmpty()) values.add(Double.parseDouble(line));
        }
        br.close();
        return values;
    }
    
    public static void main(String[] args) {
        try {
            List<Double> vals = readConstants();
            int LENGTH = vals.get(0).intValue();
            long JAVA_MULT = vals.get(9).longValue();
            long JAVA_INC = vals.get(10).longValue();
            
            StringBuilder sb = new StringBuilder();
            long seed = System.currentTimeMillis();
            for (int i = 0; i < LENGTH; i++) {
                seed = (JAVA_MULT * seed + JAVA_INC) & 0xffffffffffffL;
                sb.append((seed >> 16) % 2);
            }
            
            new File("results").mkdirs();
            PrintWriter out = new PrintWriter("results/sequence_java.txt");
            out.print(sb.toString());
            out.close();
        } catch (Exception e) {
            e.printStackTrace();
        }
    }
}