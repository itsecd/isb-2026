#include <stdio.h>
#include <stdlib.h>

void gen_rand(int seed, int n, const char *name)
{
  srand(seed);
  FILE *file = fopen(name, "w");
  if (!file)
    perror("the file did not open");
    return;

  for (int i = 0; i < n; ++i)
  {
    int elem = (rand() / (RAND_MAX / 2 + 1)) % 2;
    fprintf(file, "%d", elem);
  }

  fclose(file);
}

int main()
{
  int n = 128;
  int seed = 11342;

  gen_rand(seed, n, "generate_c.txt");
}