#include <stdio.h>
#include <math.h>
#include <gsl/gsl_errno.h>
#include <gsl/gsl_matrix.h>
#include <gsl/gsl_odeiv2.h>

/* Układ:
   x' = x(1 - y)
   y' = y(x - 1)
*/

int func(double t, const double y[], double f[], void *params)
{
    (void)t;      // t nieużywany (układ autonomiczny)
    (void)params; // brak parametrów

    const double x = y[0];
    const double yy = y[1];

    f[0] = x * (1.0 - yy);   // dx/dt
    f[1] = yy * (x - 1.0);   // dy/dt

    return GSL_SUCCESS;
}

static double H_invariant(double x, double y)
{
    if (x > 0.0 && y > 0.0) {
        return x - log(x) + y - log(y);
    } else {
        return NAN;
    }
}

int main(void)
{
    /* Warunki początkowe – możesz zmienić */
    const double x0 = 1.5;
    const double y0 = 0.6;

    const double dt = 1e-3;     // krok czasowy
    const int    nsteps = 10000; // liczba kroków (tu: do t ≈ 10)

    int s = GSL_SUCCESS;

    /* Układ 2-wymiarowy: y[0]=x, y[1]=y */
    gsl_odeiv2_system sys = { func, NULL, 2, NULL };


    gsl_odeiv2_driver *d =
        gsl_odeiv2_driver_alloc_y_new(&sys, gsl_odeiv2_step_rk4,
                                      dt, 1e-6, 1e-6);

    double t = 0.0;
    double y[2] = { x0, y0 };

    FILE *fp = fopen("wynik_lv.txt", "w");
    if (!fp) {
        perror("Nie mogę otworzyć pliku wynik_lv.txt");
        gsl_odeiv2_driver_free(d);
        return 1;
    }

    /* Nagłówek: t, x, y, H (jeśli x,y>0) */
    fprintf(fp, "# t\tx\ty\tH(x,y)\n");
    fprintf(fp, "%.8e\t%.12e\t%.12e\t%.12e\n", t, y[0], y[1], H_invariant(y[0], y[1]));

    for (int i = 0; i < nsteps; i++) {
        s = gsl_odeiv2_driver_apply_fixed_step(d, &t, dt, 1, y);
        if (s != GSL_SUCCESS) {
            fprintf(stderr, "error: driver returned %d\n", s);
            break;
        }

        const double x = y[0];
        const double yy = y[1];
        const double H = H_invariant(x, yy);

        fprintf(fp, "%.8e\t%.12e\t%.12e\t%.12e\n", t, x, yy, H);
    }

    fclose(fp);
    gsl_odeiv2_driver_free(d);
    return s;
}
