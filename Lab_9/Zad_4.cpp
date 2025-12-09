#include <iostream>
#include <fstream>
#include <cmath>

using namespace std;

int main()
{
  
    const double b = 0.30;
    const int N = 1000;       
    const int N_skip = 700;   
    const int A_STEPS = 2000;
    double a_min = 0.0;
    double a_max = 1.5;

    ofstream file("bifurcation2.txt");

    for (int i = 0; i < A_STEPS; i++)
    {
        double a = a_min + (a_max - a_min) * i / (A_STEPS - 1);

        double x = -0.2;
        double y = 0.2;


        for (int n = 0; n < N; n++)
        {
            double xn = 1.0 - a * x * x + y;
            double yn = b * x;

            x = xn;
            y = yn;

            if (n >= N_skip)
            {
                file << a << " " << x << "\n";
            }
        }
    }

    file.close();
    return 0;
}
