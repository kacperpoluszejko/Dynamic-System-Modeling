#include <stdio.h>
#include <math.h>
#include <gsl/gsl_errno.h>
#include <gsl/gsl_odeiv2.h>

int rhs(double t, const double y[], double f[], void *params)
{
    (void)t;     
    (void)params; 
    const double r = y[0]; 
    const double th = y[1]; 

  
    f[0] = -r*(pow(r, 4) -4*r*r + 1);
   
    f[1] = 2;

    return GSL_SUCCESS;
}

int main(void)
{
    const double dt     = 1e-3;     
    const int    nsteps = 10000;     

    const double ic[][2] = {
        {  0.2,  0 },
        {  0.4,  0 },
        {  0.5175,  0 },
        {  0.5180,  0 },
        {  1.0,  0 },
        {  1.8,  0 },
        {  2.5,  0 }
    };
    const int NRUNS = (int)(sizeof(ic)/sizeof(ic[0]));


    gsl_odeiv2_system sys;
    sys.function = rhs;
    sys.jacobian = NULL;   
    sys.dimension = 2;    
    sys.params = NULL;

    for (int run = 0; run < NRUNS; ++run) {
        double t = 0.0;
        double y[2] = { ic[run][0], ic[run][1] }; // y[0]=x, y[1]=y

        gsl_odeiv2_driver *d =
            gsl_odeiv2_driver_alloc_y_new(&sys, gsl_odeiv2_step_rk4,
                                          dt, 1e-6, 1e-6);
        if (!d) {
            fprintf(stderr, "Nie udało się zaalokować drivera (run=%d)\n", run);
            return 1;
        }

        char fname[256];
        snprintf(fname, sizeof(fname), "traj_%02d.txt", run + 1);

        FILE *fp = fopen(fname, "w");
        if (!fp) {
            perror("Nie mogę otworzyć pliku wyjściowego");
            gsl_odeiv2_driver_free(d);
            return 1;
        }

        fprintf(fp, "# Układ: x' = x(y-1),  y' = 3x - 2y + x^2 - 2y^2\n");
        fprintf(fp, "# IC: x0=%.6g, y0=%.6g, dt=%.3e, nsteps=%d\n", y[0], y[1], dt, nsteps);
        fprintf(fp, "# t\tx(t)\ty(t)\n");

        fprintf(fp, "%.8e\t%.12e\t%.12e\n", t, y[0], y[1]);


        for (int i = 0; i < nsteps; ++i) {
            int s = gsl_odeiv2_driver_apply_fixed_step(d, &t, dt, 1, y);
            if (s != GSL_SUCCESS) {
                fprintf(stderr, "error: driver returned %d (run=%d, step=%d)\n", s, run, i);
                break;
            }
            fprintf(fp, "%.8e\t%.12e\t%.12e\n", t, y[0], y[1]);
        }

        fclose(fp);
        gsl_odeiv2_driver_free(d);
        printf("Zapisano: %s (IC: x0=%.3g, y0=%.3g)\n", fname, ic[run][0], ic[run][1]);
    }

    return 0;
}
