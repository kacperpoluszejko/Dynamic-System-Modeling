#include <iostream>
#include <fstream>
#include <cmath>
#include <sstream>

using namespace std;



string clean_number(double a)
{
    std::ostringstream oss;
    oss << a;   
    return oss.str();
}


template<typename T>
void poincare(const string& filename, T a, T b)
{
    ofstream file(filename);

    int N = 20000;      
    int N_skip = 200;  

    T x = 0.1;
    T y = 0.1;

    for (int i = 0; i < N; i++)
    {
        T xn = 1 - a * x * x + y;
        T yn = b * x;

        x = xn;
        y = yn;

        if (i >= N_skip)
            file << x << " " << y << "\n";
    }

    file.close();
}

int main()
{
    double a_vals[4] = {0.50, 1.10, 1.25, 1.40};
    double b = 0.30;

    for (int i = 0; i < 4; i++)
    {
        double a = a_vals[i];
        
        poincare<double>("poincare_double_a_" + to_string(a) + ".txt", a, b);
        poincare<float>("poincare_float_a_" + to_string(a) + ".txt", (float)a, (float)b);
    }

    return 0;
}
