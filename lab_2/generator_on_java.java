import java.security.SecureRandom;

public class Random128Bit {
    public static void main(String[] args) {
        SecureRandom random = new SecureRandom();

        byte[] bytes = new byte[16]; // 128 бит = 16 байт
        random.nextBytes(bytes);

        StringBuilder binaryString = new StringBuilder();
        for (byte b : bytes) {
            binaryString.append(String.format("%8s", Integer.toBinaryString(b & 0xFF)).replace(' ', '0'));
        }

        System.out.println(binaryString.toString());
    }
}