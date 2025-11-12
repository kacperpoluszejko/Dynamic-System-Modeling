#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <gsl/gsl_errno.h>
#include <gsl/gsl_matrix.h>
#include <gsl/gsl_odeiv2.h>

typedef struct {
    double m;
} params_t;

int func(double t, const double y[], double f[], void *params)
{
    (void)t;
    params_t *p = (params_t*)params;
    f[0] = y[0]*y[0]*y[0]+y[0]*y[0]-2*y[0]- p->m*y[0] + p->m;
    return GSL_SUCCESS;
}


int main(void)
{

    const double dt     = 1e-3;
    const int    nsteps = 2000;   


    double m_list[] = { -3};
    const int NM = (int)(sizeof(m_list)/sizeof(m_list[0]));


    const double x0_min = -4.0, x0_max = 2.0, dx0 = 0.2;
    const int N_IC = (int)floor((x0_max - x0_min)/dx0 + 0.5) + 1;

    double *x0_list = (double*)malloc(N_IC * sizeof(double));
    if (!x0_list) { fprintf(stderr, "Brak pamięci\n"); return 1; }
    for (int i = 0; i < N_IC; ++i) x0_list[i] = x0_min + i*dx0;

    for (int im = 0; im < NM; ++im) {
        double m = m_list[im];
        params_t par = { .m = m };

        gsl_odeiv2_system sys = { func, NULL, 1, &par };

        for (int i0 = 0; i0 < N_IC; ++i0) {
            double t = 0.0;
            double y[1] = { x0_list[i0] };

            gsl_odeiv2_driver *d =
                gsl_odeiv2_driver_alloc_y_new(&sys, gsl_odeiv2_step_rk4,
                                              dt, 1e-6, 1e-6);
            if (!d) {
                fprintf(stderr, "Nie udało się zaalokować drivera (m=%g, x0=%g)\n", m, x0_list[i0]);
                free(x0_list);
                return 1;
            }

            char fname[256];
            snprintf(fname, sizeof(fname),
                     "traj_m_%+.3f_x0_%+.2f.txt", m, x0_list[i0]);
            FILE *fp = fopen(fname, "w");
            if (!fp) {
                perror("Nie mogę otworzyć pliku wyjściowego");
                gsl_odeiv2_driver_free(d);
                free(x0_list);
                return 1;
            }

            fprintf(fp, "# xdot = m - |x|, m=%.6g, x0=%.6g, dt=%.3e, nsteps=%d\n",
                    m, y[0], dt, nsteps);
            fprintf(fp, "# t\tx\n");

            for (int k = 0; k < nsteps; ++k) {
                int s = gsl_odeiv2_driver_apply_fixed_step(d, &t, dt, 1, y);
                if (s != GSL_SUCCESS) {
                    fprintf(stderr, "Błąd GSL=%d (m=%g, x0=%g, step=%d)\n", s, m, x0_list[i0], k);
                    break;
                }
                fprintf(fp, "%.10e\t%.12e\n", t, y[0]);
            }

            fclose(fp);
            gsl_odeiv2_driver_free(d);
            printf("Zapisano: %s\n", fname);
        }

    }

    free(x0_list);
    return 0;
}
