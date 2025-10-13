#include <stdio.h>
#include <gsl/gsl_errno.h>
#include <gsl/gsl_matrix.h>
#include <gsl/gsl_odeiv2.h>

int
func (double, const double y[], double f[],
      void *)
{
  f[0] = y[0]*y[0];
  return GSL_SUCCESS;
}

double yexact(double x, double y0)
{
  return 1.0/ ( ( 1.0/y0 ) - x);
}

int
main (void)
{
  gsl_odeiv2_system sys = { func, nullptr, 2, nullptr };

  gsl_odeiv2_driver *d =
    gsl_odeiv2_driver_alloc_y_new (&sys, gsl_odeiv2_step_rk4,
                                   1e-3, 1e-6, 1e-6);

  double t = 0.0;
  double y[2] = { 0.5 };
  int i, s;

  FILE *fp = fopen("wynik5.txt", "w");
  if (!fp) {
      perror("Nie mogę otworzyć pliku wynik.txt");
      return 1;
  }

  for (i = 0; i < 1000; i++)
    {
      s = gsl_odeiv2_driver_apply_fixed_step (d, &t, 1e-3, 1, y);

      if (s != GSL_SUCCESS)
        {
          printf ("error: driver returned %d\n", s);
          break;
        }


      fprintf(fp, "%.5e %.5e %.5e\n", t, y[0], y[1]);
    }

  fclose(fp); 

  gsl_odeiv2_driver_free (d);
  return s;
}
