import java.io.PrintWriter;
import java.io.IOException;
import java.util.Random;

public class Main
{
    public static void main(String[] args)
	{
        Random rand = new Random();
        try (PrintWriter out = new PrintWriter("C:\\Users\\Адель\\Desktop\\Лаб 2\\isb-2026\\lab_2\\ГПСЧ Java\\Java_sequence.txt"))
		{
            for (int i = 0; i < 128; i++)
			{
                out.print(rand.nextInt(2));
            }
			
            System.out.println("Последовательность Java сохранена в sequence_java.txt");
        }
		catch (IOException e) 
		{
            System.err.println("Ошибка при записи файла: " + e.getMessage());
        }
    }
}