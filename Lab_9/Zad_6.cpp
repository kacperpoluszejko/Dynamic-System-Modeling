#include <iostream>
#include <fstream>
#include <cmath>
#include <string>
#include <sstream>

using namespace std;

string clean_number(double a)
{
    std::ostringstream oss;
    oss << a;   
    return oss.str();
}

//Wersja z wieloma punktami początkowymi
template<typename T>
void poincare_multi(const string& filename, T a, T b)
{
    ofstream file(filename);

    const int N = 2000;        
    const int N_skip = 400;    
    const int S = 80;          

    for (int s = 0; s < S; s++)
    {

        T x = (T)(0.5 * cos(0.1 * s));
        T y = (T)(0.5 * sin(0.1 * s));

        for (int i = 0; i < N; i++)
        {
            T xn = (T)(1.0 - a * x * x + y);
            T yn = (T)(b * x);

            x = xn;
            y = yn;

            if (i >= N_skip)
                file << x << " " << y << "\n";
        }
    }

    file.close();
}

int main()
{
    double a_vals[4] = {0.50, 1.10, 1.25, 1.40};
    double b = 0.30;

    for (double a : a_vals)
    {
        string a_str = clean_number(a);

        string file_d = "poincare_multi_double_a_" + a_str + ".txt";
        poincare_multi<double>(file_d, a, b);

        string file_f = "poincare_multi_float_a_" + a_str + ".txt";
        poincare_multi<float>(file_f, (float)a, (float)b);
    }

    return 0;
}
