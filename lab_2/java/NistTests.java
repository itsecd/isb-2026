public class NistTests {

    public static double erf(double x) {
        double t = 1.0 / (1.0 + 0.5 * Math.abs(x));
        double tau = t * Math.exp(-x*x - 1.26551223 +
                t*(1.00002368 +
                t*(0.37409196 +
                t*(0.09678418 +
                t*(-0.18628806 +
                t*(0.27886807 +
                t*(-1.13520398 +
                t*(1.48851587 +
                t*(-0.82215223 +
                t*0.17087277)))))))));
        return x >= 0 ? 1 - tau : tau - 1;
    }

    public static double erfc(double x) {
        return 1 - erf(x);
    }

    public static double frequencyTest(String seq) {
        int sum = 0;

        for (char c : seq.toCharArray())
            sum += (c == '1') ? 1 : -1;

        double sObs = Math.abs(sum) / Math.sqrt(seq.length());
        return erfc(sObs / Math.sqrt(2.0));
    }

    public static double runsTest(String seq) {
        int N = seq.length();
        int ones = 0;

        for (char c : seq.toCharArray())
            if (c == '1') ones++;

        double pi = (double) ones / N;

        if (Math.abs(pi - 0.5) >= (2.0 / Math.sqrt(N)))
            return 0.0;

        int Vn = 1;
        for (int i = 1; i < N; i++)
            if (seq.charAt(i) != seq.charAt(i - 1))
                Vn++;

        double numerator = Math.abs(Vn - 2 * N * pi * (1 - pi));
        double denominator = 2 * Math.sqrt(2 * N) * pi * (1 - pi);

        return erfc(numerator / denominator);
    }

    public static double longestRunTest(String seq) {
        int M = 8;
        int blocks = seq.length() / M;

        int[] count = new int[4];

        for (int i = 0; i < blocks; i++) {
            int maxRun = 0;
            int currentRun = 0;

            for (int j = 0; j < M; j++) {
                if (seq.charAt(i*M + j) == '1') {
                    currentRun++;
                    maxRun = Math.max(maxRun, currentRun);
                } else {
                    currentRun = 0;
                }
            }

            if (maxRun <= 1) count[0]++;
            else if (maxRun == 2) count[1]++;
            else if (maxRun == 3) count[2]++;
            else count[3]++;
        }

        double[] pi = {0.2148, 0.3672, 0.2305, 0.1875};
        double chi2 = 0;

        for (int i = 0; i < 4; i++) {
            double expected = blocks * pi[i];
            chi2 += (count[i] - expected)*(count[i] - expected)/expected;
        }

        return Math.exp(-chi2 / 2.0);
    }
}