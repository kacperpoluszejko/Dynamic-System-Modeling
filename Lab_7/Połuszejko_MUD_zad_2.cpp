#include <iostream>
#include <fstream>
#include <cmath>

using namespace std;

int main()
{
double a=2.83;
int t=300;
double xn, xn1;

ofstream plik1("C:\\Users\\kacpe\\OneDrive\\Pulpit\\Programming\\FUZ\\FUZ_2\\MUD_6.txt");
if(!plik1.is_open()) {
    cout << "Nie mozna otworzyc pliku!\n";
    return 1;
}

double x0[4] = {-0.8, -0.3, 0.2, 0.7};

for (int j = 0; j<4; j++)
{
    xn = x0[j];
    for (int i=0; i<t; i++)
    {
        plik1<<i<<" "<<xn<<endl;
        xn1 = a*xn - xn*xn*xn;
        xn=xn1;

    }
    plik1<<endl;
}
std::cout<<"Koniec";

return 0;
}