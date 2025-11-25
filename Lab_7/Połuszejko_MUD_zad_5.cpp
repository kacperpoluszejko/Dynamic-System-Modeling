#include <iostream>
#include <fstream>
#include <cmath>
using namespace std;

double lapunov(double a, double x0)
{
    int N = 300;
    int transient = 200;

    double x = x0;

    for (int i = 0; i < transient; i++)
        x = a*x - x*x*x;

    double sum = 0.0;

    for (int i = 0; i < N; i++)
    {
        double fp = a - 3*x*x;
        sum += log(fabs(fp));

        x = a*x - x*x*x;
    }

    return sum / N;
}

int main()
{
    ofstream plik1("MUD_33.txt");

    for (int i = 0; i < 601; i++)
    {
        double a = 0.005*i;   
        double lambda = lapunov(a, 0.2);

        plik1 << a << " " << lambda << endl;
    }

    plik1.close();
    cout << "Koniec\n";
}
