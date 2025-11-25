#include <iostream>
#include <fstream>
#include <cmath>

using namespace std;

int main()
{
double x0=0.8;
int t=1000;
double xn, xn1, r;

ofstream plik1("C:\\Users\\kacpe\\OneDrive\\Pulpit\\Programming\\FUZ\\FUZ_2\\MUD_23.txt");

double r_table[401];

for (int i =0; i<401; i++)
{
    r_table[i] = 0.005*i+0.7;
}


for (int j = 0; j<401; j++)
{
    xn=x0;
    r = r_table[j];
    // cout<<j;
    for (int i=0; i<=t; i++)
    {
        if (i>200) plik1<<r<<" "<<xn<<endl;

        xn1 = r*xn-xn*xn*xn;
        xn=xn1;

    }
    plik1<<endl;
}
cout<<"Koniec";

return 0;
}