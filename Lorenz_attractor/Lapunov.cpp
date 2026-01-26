#include <stdio.h>
#include <math.h>
#include <gsl/gsl_errno.h>
#include <gsl/gsl_odeiv2.h>

typedef struct {
    double sigma;
    double rho;
    double beta;
} Params;

/* Prawa strona układu Lorenza: y = (x,y,z), f = (dx/dt, dy/dt, dz/dt) */
int rhs(double t, const double y[], double f[], void *params)
{
    (void)t;
    Params *p = (Params*)params;

    f[0] = p->sigma * (y[1] - y[0]);
    f[1] = y[0] * (p->rho - y[2]) - y[1];
    f[2] = y[0] * y[1] - p->beta * y[2];

    return GSL_SUCCESS;
}

/* Norma euklidesowa w R^3 */
static double norm3(const double v[3])
{
    return sqrt(v[0]*v[0] + v[1]*v[1] + v[2]*v[2]);
}

int main(void)
{
    /* Stałe parametry układu Lorenza */
    const double sigma = 10.0;
    const double beta  = 8.0/3.0;

    /* Parametry całkowania i zaburzenia początkowego */
    const double dt = 1e-3;
    const double d0 = 1e-7;

    /* Czas transjentu, czas uśredniania i interwał renormalizacji */
    const double T_trans  = 20.0;
    const double T_total  = 200.0;
    const double T_renorm = 0.1;

    /* Liczba kroków odpowiadająca powyższym czasom */
    const int n_trans  = (int)llround(T_trans / dt);
    const int n_total  = (int)llround(T_total / dt);
    const int n_renorm = (int)llround(T_renorm / dt);

    /* Zakres i liczba próbek parametru rho */
    const double rho_min = 0.5;
    const double rho_max = 28.0;
    const int NRHO = 100;

    /* Plik wyjściowy: rho oraz największy wykładnik Lapunova */
    FILE *fp = fopen("lyapunov_vs_rho.txt", "w");
    fprintf(fp, "# rho lambda_max\n");

    for (int ir = 0; ir < NRHO; ++ir) {

        /* Równomierna siatka rho w przedziale [rho_min, rho_max] */
        double rho = rho_min + (rho_max - rho_min) * (double)ir / (double)(NRHO - 1);

        Params params = { sigma, rho, beta };

        /* Definicja układu ODE dla GSL */
        gsl_odeiv2_system sys;
        sys.function = rhs;
        sys.jacobian = NULL;
        sys.dimension = 3;
        sys.params = &params;

        /* Dwa niezależne drivery: trajektoria bazowa i trajektoria zaburzona */
        gsl_odeiv2_driver *d1 =
            gsl_odeiv2_driver_alloc_y_new(&sys, gsl_odeiv2_step_rk4,
                                          dt, 1e-9, 1e-9);

        gsl_odeiv2_driver *d2 =
            gsl_odeiv2_driver_alloc_y_new(&sys, gsl_odeiv2_step_rk4,
                                          dt, 1e-9, 1e-9);

        double t1 = 0.0;
        double t2 = 0.0;

        /* Warunek początkowy dla trajektorii bazowej */
        double y1[3] = { 1.0, 1.0, params.rho - 1.0 };

        /* Trajektoria zaburzona: dodanie małego odchylenia d0 */
        double y2[3] = { y1[0] + d0, y1[1], y1[2] };

        /* Integracja transjentu: odrzucenie początkowego przejścia */
        for (int i = 0; i < n_trans; ++i) {
            int s1 = gsl_odeiv2_driver_apply_fixed_step(d1, &t1, dt, 1, y1);
            int s2 = gsl_odeiv2_driver_apply_fixed_step(d2, &t2, dt, 1, y2);
            if (s1 != GSL_SUCCESS || s2 != GSL_SUCCESS) break;
        }

        /* Sumowanie logarytmów rozciągnięć i licznik renormalizacji */
        double sum_log = 0.0;
        int nblocks = 0;

        /* Główna pętla do estymacji lambda_max */
        for (int i = 0; i < n_total; ++i) {
            int s1 = gsl_odeiv2_driver_apply_fixed_step(d1, &t1, dt, 1, y1);
            int s2 = gsl_odeiv2_driver_apply_fixed_step(d2, &t2, dt, 1, y2);
            if (s1 != GSL_SUCCESS || s2 != GSL_SUCCESS) break;

            /* Co n_renorm kroków: pomiar separacji i renormalizacja */
            if ((i + 1) % n_renorm == 0) {

                /* Wektor różnicy pomiędzy trajektoriami */
                double dv[3] = { y2[0] - y1[0], y2[1] - y1[1], y2[2] - y1[2] };
                double d = norm3(dv);

                if (d > 0.0) {

                    /* Lokalne rozciągnięcie: log(d/d0) */
                    sum_log += log(d / d0);

                    /* Renormalizacja odchylenia do wartości d0 */
                    double scale = d0 / d;
                    y2[0] = y1[0] + dv[0] * scale;
                    y2[1] = y1[1] + dv[1] * scale;
                    y2[2] = y1[2] + dv[2] * scale;

                    nblocks += 1;
                }
            }
        }

        /* Estymator największego wykładnika Lapunova */
        double lambda = 0.0;
        if (nblocks > 0) lambda = sum_log / (nblocks * T_renorm);

        /* Zapis wyniku do pliku i wypisanie postępu */
        fprintf(fp, "%.10f\t%.12e\n", rho, lambda);
        printf("%3d/%d  rho=%.6f  lambda_max=%.6e\n", ir + 1, NRHO, rho, lambda);

        gsl_odeiv2_driver_free(d1);
        gsl_odeiv2_driver_free(d2);
    }

    fclose(fp);
    return 0;
}
