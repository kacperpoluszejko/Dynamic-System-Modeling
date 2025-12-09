#include <iostream>
#include <fstream>
#include <cmath>

using namespace std;

int main()
{
    float a[4] = {0.50, 1.10, 1.25, 1.40};
    float b = 0.30;

    int N = 1000;      
    int N_skip = 200;  

    for (int k = 0; k < 4; k++)
    {
        float x = 0.0, y = 0.0;
        float xn, yn;

        string filename = "henon_a_float" + to_string(a[k]) + ".txt";
        ofstream file(filename);

        for (int i = 0; i < N; i++)
        {
            xn = 1.0 - a[k] * x * x + y;
            yn = b * x;

            x = xn;
            y = yn;

            if (i >= N_skip)
                file << x << " " << y << "\n";
        }
        file.close();
    }

    return 0;
}


