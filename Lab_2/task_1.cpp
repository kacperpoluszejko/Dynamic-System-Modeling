#include <stdio.h>
#include <math.h>
#include <gsl/gsl_errno.h>
#include <gsl/gsl_matrix.h>
#include <gsl/gsl_odeiv2.h>

int func(double t, const double y[], double f[], void *params)
{
    (void)t;      // t nieużywany
    (void)params; // params nieużywane
    double k = -1;
    f[0] = k * y[0] * ( 1 - y[0] );
    return GSL_SUCCESS;
}

// double yexact(double x, double y0)
// {
//     return 1.0 / ((1.0 / y0) - x);
// }

int main(void)
{
    const double y0 = 2;       // warunek początkowy
    const double dt = 1e-3;      // krok czasowy
    const int    nsteps = 3000;  // liczba kroków (do t = 1.0)
    int s = GSL_SUCCESS;

    // Układ 1-wymiarowy (tylko y[0])
    gsl_odeiv2_system sys = { func, NULL, 1, NULL };

    gsl_odeiv2_driver *d =
        gsl_odeiv2_driver_alloc_y_new(&sys, gsl_odeiv2_step_rk4,
                                      dt, 1e-3, 1e-3);

    double t = 0.0;
    double y[1] = { y0 };

    FILE *fp = fopen("wynik_16.txt", "w");
    if (!fp) {
        perror("Nie mogę otworzyć pliku wynik5.txt");
        gsl_odeiv2_driver_free(d);
        return 1;
    }

    // Nagłówek kolumn: t, y_num, y_exact, abs_err, rel_err
    fprintf(fp, "# t\ty_num\ty_exact\tabs_err\trel_err\n");

    for (int i = 0; i < nsteps; i++) {
        s = gsl_odeiv2_driver_apply_fixed_step(d, &t, dt, 1, y);
        if (s != GSL_SUCCESS) {
            fprintf(stderr, "error: driver returned %d\n", s);
            break;
        }

        double y_num = y[0];
        double y_ex  = 1; // yexact(t, y0);
        double abs_err = fabs(y_num - y_ex);
        double rel_err = (fabs(y_ex) > 0.0) ? abs_err / fabs(y_ex) : NAN;

        fprintf(fp, "%.8e\t%.12e\t%.12e\t%.12e\t%.12e\n",
                t, y_num, y_ex, abs_err, rel_err);
    }

    fclose(fp);
    gsl_odeiv2_driver_free(d);
    return s;
}
