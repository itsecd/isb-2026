#include <iostream>
#include <fstream>
#include <filesystem>
#include <random>
#include <vector>


using namespace std;
using namespace std::filesystem;

vector<int> generate_random_vector(size_t size)
{
  random_device seed;
  default_random_engine e(seed());
  uniform_int_distribution d(0, 1);

  vector<int> m(size);
  for (int i = 0;i < size;i++)
  {
    m[i] = d(e);
  }
  return m;
}

ostream& operator<<(ostream& os, const vector<int>& v)
{
  for (int i = 0;i < v.size();i++)
  {
    os << v[i];
  }
  return os;
}

void save_vector(filesystem::path file_name, const vector<int>& v)
{
  filesystem::path directorypath = "../../../";
  ofstream file(directorypath / file_name);
  file << v;
}

int main()
{
    try
    {
        vector<int> v = generate_random_vector(128);
        cout << v << "\n";
        save_vector("cpp_random_vec.txt", v);
    }
    catch (const char* e)
    {
        cerr << e;
    }
    return 0;
}
