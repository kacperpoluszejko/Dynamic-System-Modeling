#include <stdio.h>
#include <math.h>
#include <gsl/gsl_errno.h>
#include <gsl/gsl_odeiv2.h>

// ------------------------------------------------------------
// PRAWA STRONA UKŁADU – TERAZ z parametrem m
// ------------------------------------------------------------
int rhs(double t, const double y[], double f[], void *params)
{
    (void)t;
    const double m = *(const double*)params;  // <-- ODCZYT PARAMETRU m

    const double x = y[0]; 
    const double z = y[1]; 

    f[0] = z;
    f[1] = -3.0*(x*x - 1.0)*z - x + m;   // poprawne równanie eps = 3

    return GSL_SUCCESS;
}

// ------------------------------------------------------------
// PROGRAM GŁÓWNY
// ------------------------------------------------------------
int main(void)
{
    const double dt     = 1e-4;
    const int    nsteps = 100000;

    // -----------------------------------------
    // LISTA wartości m – dokładnie tak jak chciałeś
    // -----------------------------------------
    const double m_list[] = {
        0.2,
        1.0/sqrt(3.0),
        0.8,
        1.2,
        1.0,
        sqrt(5.0/3.0),
        2.5
    };
    const int NM = sizeof(m_list)/sizeof(m_list[0]);

    // Warunki początkowe jak wcześniej
    const double ic[][2] = {
        {  0.2,   0   },
        {  1.0,   1.0 },
        {  3.0,   2.5 },
        { -3.0,  -3.0 },
        {  2.0,   0.0 },
        {  -2.0,   0.0 },
        {  -1.0,   -2.0 },
    };
    const int NRUNS = sizeof(ic)/sizeof(ic[0]);

    // -----------------------------------------
    // PĘTLA po wartościach m
    // -----------------------------------------
    for(int k = 0; k < NM; ++k)
    {
        double m = m_list[k];
        printf("\n=== SYMULACJA DLA m = %.10f ===\n", m);

        // System dla GSL
        gsl_odeiv2_system sys;
        sys.function  = rhs;
        sys.jacobian  = NULL;
        sys.dimension = 2;
        sys.params    = &m;  // <-- PRZEKAZANIE parametru

        // PĘTLA po warunkach początkowych
        for (int run = 0; run < NRUNS; ++run)
        {
            double t = 0.0;
            double y[2] = { ic[run][0] + m, ic[run][1] }; 
            // ^ jeśli chcesz przesunięcie IC o m, jak w Twoim kodzie

            gsl_odeiv2_driver *d =gsl_odeiv2_driver_alloc_y_new(&sys, gsl_odeiv2_step_rk4, dt, 1e-6, 1e-6);

            if (!d) {
                fprintf(stderr, "Błąd alokacji drivera!\n");
                return 1;
            }

            // Nazwa pliku: traj_m_<m>_run<nr>.txt
            char fname[256];
            snprintf(fname, sizeof(fname),
                     "traj_m_%0.5f_run%d.txt", m, run+1);

            FILE *fp = fopen(fname, "w");
            if (!fp) {
                perror("Nie mogę otworzyć pliku");
                gsl_odeiv2_driver_free(d);
                return 1;
            }

            fprintf(fp, "# Trajektoria dla m = %.10f\n", m);
            fprintf(fp, "# IC: x0=%.6g, z0=%.6g\n", y[0], y[1]);
            fprintf(fp, "# t\tx(t)\tz(t)\n");

            fprintf(fp, "%.8e\t%.12e\t%.12e\n", t, y[0], y[1]);

            for (int i = 0; i < nsteps; ++i) {
                int s = gsl_odeiv2_driver_apply_fixed_step(d, &t, dt, 1, y);
                if (s != GSL_SUCCESS) {
                    fprintf(stderr,
                            "GSL error %d (m=%g, run=%d, step=%d)\n",
                            s, m, run, i);
                    break;
                }
                fprintf(fp, "%.8e\t%.12e\t%.12e\n", t, y[0], y[1]);
            }

            fclose(fp);
            gsl_odeiv2_driver_free(d);

            printf("Zapisano: %s\n", fname);
        }
    }

    return 0;
}
