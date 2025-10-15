#include <stdio.h>
#include <math.h>
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

/* czas osobliwości (jeśli istnieje w przyszłości) dla rozwiązania logistycznego:
   1 + ((1 - x0)/x0) * exp(-k * t) = 0  =>  t* = -(1/k) * ln( -x0/(1-x0) ),
   istnieje tylko gdy -x0/(1-x0) > 0, tj. x0 < 0 lub x0 > 1. */
int has_future_blowup(double x0, double k, double *tstar_out)
{
    if (x0 < 0.0 || x0 > 1.0) {
        double arg = -x0 / (1.0 - x0);
        if (arg > 0.0) {
            double tstar = -(1.0/k) * log(arg);
            if (tstar > 0.0) { // osobliwość w przyszłości
                if (tstar_out) *tstar_out = tstar;
                return 1;
            }
        }
    }
    return 0;
}

void integrate_and_dump(double k, const char *fname,
                        double t0, double tmax, double dt)
{
    FILE *fp = fopen(fname, "w");
    if (!fp) {
        perror("Nie mogę otworzyć pliku wyjściowego");
        return;
    }

    fprintf(fp, "# logistic: x' = k x (1 - x), k = %.1f, dt = %.3g\n", k, dt);
    fprintf(fp, "# Każdy blok: nagłówek '# x0=...' i wiersze: t\tx\n\n");

    // lista x0: -1.0, -0.8, ..., 1.8, 2.0
    const int nIC = 16; // (-1.0..2.0 co 0.2) -> 16 wartości
    double x0_list[nIC];
    for (int i = 0; i < nIC; ++i)
        x0_list[i] = -1.0 + 0.2 * i;

    for (int ic = 0; ic < nIC; ++ic) {
        double x0 = x0_list[ic];

        params_t P = { .k = k };
        gsl_odeiv2_system sys = { func, NULL, 1, &P };

        gsl_odeiv2_driver *d = gsl_odeiv2_driver_alloc_y_new(
            &sys, gsl_odeiv2_step_rk4, dt, 1e-9, 1e-9
        );

        double t = t0;
        double y[1] = { x0 };

        double t_end = tmax;
        double tstar;
        if (has_future_blowup(x0, k, &tstar)) {
            // Jedziemy minimalnie przed t*, żeby uniknąć NaN
            const double eps = 1e-6;
            if (tstar - eps < t_end) t_end = tstar - eps;
        }

        fprintf(fp, "# x0=%.6g\n", x0);
        fprintf(fp, "%.10g\t%.16g\n", t, y[0]);

        // liczba kroków potrzebna, by dojść do t_end
        long nsteps = (long)ceil((t_end - t0) / dt);
        for (long i = 0; i < nsteps; ++i) {
            int s = gsl_odeiv2_driver_apply_fixed_step(d, &t, dt, 1, y);
            if (s != GSL_SUCCESS) {
                fprintf(stderr, "GSL error (k=%.1f, x0=%.3g) code=%d\n", k, x0, s);
                break;
            }
            fprintf(fp, "%.10g\t%.16g\n", t, y[0]);
        }
        fprintf(fp, "\n"); // separator bloków
        gsl_odeiv2_driver_free(d);
    }

    fclose(fp);
}

int main(void)
{
    const double t0 = 0.0;
    const double tmax = 3.0;
    const double dt = 1e-3;

    integrate_and_dump(+1.0, "traj_k1.txt",  t0, tmax, dt);
    integrate_and_dump(-1.0, "traj_k-1.txt", t0, tmax, dt);

    return 0;
}
