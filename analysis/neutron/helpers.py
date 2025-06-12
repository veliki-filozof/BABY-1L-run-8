import math
import openmc


def get_exp_cllif_density(temp, LiCl_frac=0.695):
    """Calculates density of ClLiF [g/cc] from temperature in Celsius
    and molar concentration of LiCl. Valid for 660 C - 1000 C.
    Source:
    G. J. Janz, R. P. T. Tomkins, C. B. Allen;
    Molten Salts: Volume 4, Part 4
    Mixed Halide Melts Electrical Conductance, Density, Viscosity, and Surface Tension Data.
    J. Phys. Chem. Ref. Data 1 January 1979; 8 (1): 125–302.
    https://doi.org/10.1063/1.555590
    """
    temp = temp + 273.15  # Convert temperature from Celsius to Kelvin
    C = LiCl_frac * 100  # Convert molar concentration to molar percent

    a = 2.25621
    b = -8.20475e-3
    c = -4.09235e-4
    d = 6.37250e-5
    e = -2.52846e-7
    f = 8.73570e-9
    g = -5.11184e-10

    rho = a + b * C + c * temp + d * C**2 + e * C**3 + f * temp * C**2 + g * C * temp**2

    return rho
