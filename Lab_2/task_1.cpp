#include <stdio.h>
#include <math.h>
#include <time.h>
#include <gsl/gsl_errno.h>
#include <gsl/gsl_matrix.h>
#include <gsl/gsl_odeiv2.h>

typedef struct {
    double k;
} params_t;

int func(double t, const double y[], double f[], void *params)
{
    (void)t;
    params_t *p = (params_t*)params;
    double k = p->k;
    f[0] = k * y[0] * (1.0 - y[0]);
    return GSL_SUCCESS;
}

// Dokładne rozwiązanie dla równania logistycznego: y' = k y (1-y), K=1
static inline double y_exact(double t, double y0, double k)
{
    // y(t) = 1 / ( 1 + ((1/y0) - 1) * exp(-k t) )
    double C = (1.0 / y0) - 1.0;
    return 1.0 / (1.0 + C * exp(-k * t));
}

int main(void)
{
    // --- Konfiguracja przebiegów ---
    // Możesz dowolnie zmieniać te listy i/lub dodać kolejne pętle z innymi parametrami.
    double y0_list[] = {-0.1, 0.1, 0.9, 1.1};
    const int NRUNS = (int)(sizeof(y0_list)/sizeof(y0_list[0]));

    const double dt     = 1e-3;     // krok czasowy
    const int    nsteps = 3000;     // liczba kroków
    const double k      = 1.0;     // parametr w równaniu
    params_t par = {.k = k};

    // Układ 1D
    gsl_odeiv2_system sys = { func, NULL, 1, &par };

    for (int run = 0; run < NRUNS; ++run) {
        double t = 0.0;
        double y[1] = { y0_list[run] };

        // Alokacja drivera dla tego przebiegu (najprościej)
        gsl_odeiv2_driver *d =
            gsl_odeiv2_driver_alloc_y_new(&sys, gsl_odeiv2_step_rk4,
                                          dt, 1e-3, 1e-3);

        if (!d) {
            fprintf(stderr, "Nie udało się zaalokować drivera dla run=%d\n", run);
            return 1;
        }

        // Zbuduj nazwę pliku: wynik_01.txt, wynik_02.txt, ...
        char fname[256];
        snprintf(fname, sizeof(fname), "wynik_%02d.txt", run + 1);

        FILE *fp = fopen(fname, "w");
        if (!fp) {
            perror("Nie mogę otworzyć pliku wyjściowego");
            gsl_odeiv2_driver_free(d);
            return 1;
        }

        // Napisz nagłówek + meta-info
        fprintf(fp, "# Równanie: y' = k y (1-y), k=%.6g, y0=%.6g, dt=%.3e, nsteps=%d\n", k, y[0], dt, nsteps);
        fprintf(fp, "# t\ty_num\ty_exact\tabs_err\trel_err\n");

        for (int i = 0; i < nsteps; ++i) {
            int s = gsl_odeiv2_driver_apply_fixed_step(d, &t, dt, 1, y);
            if (s != GSL_SUCCESS) {
                fprintf(stderr, "error: driver returned %d in run %d at step %d\n", s, run, i);
                break;
            }

            double y_num   = y[0];
            double y_ex    = y_exact(t, y0_list[run], k);
            double abs_err = fabs(y_num - y_ex);
            double rel_err = (fabs(y_ex) > 0.0) ? abs_err / fabs(y_ex) : NAN;

            fprintf(fp, "%.8e\t%.12e\t%.12e\t%.12e\t%.12e\n",
                    t, y_num, y_ex, abs_err, rel_err);
        }

        fclose(fp);
        gsl_odeiv2_driver_free(d);
        printf("Zapisano: %s\n", fname);
    }

    return 0;
}
