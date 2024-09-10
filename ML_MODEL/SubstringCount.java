import java.util.Scanner;

public class SubstringCount {

    public static int totalCount(int n, String s) {
        int mod = 1000000007;
        char target = s.charAt(0);  // The character to match
        long result = 0;

        for (int i = 0; i < n; i++) {
            if (s.charAt(i) == target) {
                // Calculate number of substrings starting at position i
                long count = n - i;  // Number of substrings starting from i to end
                result = (result + count) % mod;
            }
        }

        return (int) result;
    }

    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        int n = sc.nextInt();
        String s = sc.next();
        System.out.println(totalCount(n, s));
    }
}
