#include <stdio.h>
#include <math.h>
#include <gsl/gsl_errno.h>
#include <gsl/gsl_odeiv2.h>

typedef struct {
    double sigma;
    double rho;
    double beta;
} Params;

int rhs(double t, const double y[], double f[], void *params)
{
    (void)t;
    Params *p = (Params*)params;

    f[0] = p->sigma * (y[1] - y[0]);
    f[1] = y[0] * (p->rho - y[2]) - y[1];
    f[2] = y[0] * y[1] - p->beta * y[2];

    return GSL_SUCCESS;
}

int main(void)
{
    const double dt = 1e-3;
    const int nsteps = 50000;


    const double rho_vals[] = {28.0};
    const int NRHO = sizeof(rho_vals)/sizeof(rho_vals[0]);

    for (int r = 0; r < NRHO; ++r) {
        Params params = { 10.0, rho_vals[r], 8.0/3.0 };

        gsl_odeiv2_system sys;
        sys.function = rhs;
        sys.jacobian = NULL;
        sys.dimension = 3;
        sys.params = &params;

        const double ic[][3] = {
        { 1.0, 1.0, params.rho - 1 },
        { -1.0, -1.0, params.rho - 1 },
        { -1.0, 1.0, params.rho - 1 },
        { 1.0, -1.0, params.rho - 1 }
        };
        const int NRUNS = sizeof(ic)/sizeof(ic[0]);


        for (int run = 0; run < NRUNS; ++run) {
            double t = 0.0;
            double y[3] = { ic[run][0], ic[run][1], ic[run][2] };

            gsl_odeiv2_driver *d =
                gsl_odeiv2_driver_alloc_y_new(&sys, gsl_odeiv2_step_rk4,
                                              dt, 1e-6, 1e-6);

            char fname[256];
            snprintf(fname, sizeof(fname),
                     "lorenz_rho_%06.2f_ic_%02d.txt", params.rho, run + 1);

            FILE *fp = fopen(fname, "w");

            fprintf(fp, "# rho=%.6g\n", params.rho);
            fprintf(fp, "# t x y z\n");

            fprintf(fp, "%.8e\t%.12e\t%.12e\t%.12e\n", t, y[0], y[1], y[2]);

            for (int i = 0; i < nsteps; ++i) {
                int s = gsl_odeiv2_driver_apply_fixed_step(d, &t, dt, 1, y);
                if (s != GSL_SUCCESS) break;
                fprintf(fp, "%.8e\t%.12e\t%.12e\t%.12e\n", t, y[0], y[1], y[2]);
            }

            fclose(fp);
            gsl_odeiv2_driver_free(d);

            printf("rho=%.2f  IC=%d  zapisano %s\n", params.rho, run + 1, fname);
        }
    }

    return 0;
}
