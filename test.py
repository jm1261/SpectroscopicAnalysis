import scipy.constants as const
import numpy as np
import matplotlib.pyplot as plt
import math

"""Note that the old storage path works, but can just call "k:\\" in the path"""

"""There is something not quite right about this function but I don't know what"""

Einf = 2.033
UV_amp = 37.6569
UV_En = 11.360
IR_amp = 0.7464
Amp = 21.3130
Br = 0.890
Eo = 3.723
Eg = 1.244

wavelength_range = range(400, 1001, 1)
wavelength_m = [x * 1E-9 for x in wavelength_range]
energy_range = [(const.h * const.speed_of_light) / x for x in wavelength_m]
eV_range = [E / const.elementary_charge for E in energy_range]


IR_pole = [(IR_amp) / (0 - e) for e in eV_range]
UV_pole = [(UV_amp) / (UV_En - e) for e in eV_range]
permittivity = [Einf + I + U for I, U in zip(IR_pole, UV_pole)]

tauc = []
for e in eV_range:
    if e > Eg:
        epsilon = ((Amp*Eo*Br*((e-Eg)**2))/(((e**2-Eo**2)**2)+(Br**2)*(e**2)))*(1/e)
    else:
        epsilon = 0
    tauc.append(epsilon)


gamma = np.sqrt((Eo**2) - ((Br**2)/2))
alpha = np.sqrt((4 * (Eo**2)) - (Br**2))

def chi(E, gamma, alpha, C):
    return (((E**2)-(gamma**2))**2)+(((alpha**2)*(C**2))/4)
def a_atan(E, Eo, Eg, C):
    return ((E**2)-(Eo**2))*((Eo**2)+(Eg**2))+((Eg**2)*(C**2))
def a_in(Eg, Eo, E, C):
    return ((Eg**2)-(Eo**2))*(E**2)+((Eg**2)*(C**2))-(Eo**2)*((Eo**2)+(3*(Eg**2)))

def first_function(Eo, Eg, a, A, C, E, g):
    logarithm = np.log(((Eo**2)+(Eg**2)+(a*Eg)) / ((Eo**2)+(Eg**2)-(a*Eg)))
    fractions = (1/2)*(A/np.pi)*(C/chi(E, g, a, C))
    return fractions * logarithm
def second_function(A, Eo, Eg, a, C, E, g):
    fractions = ((A/(np.pi*chi(E, g, a, C)))*(a_atan(E, Eo, Eg, C)/Eo))
    brackets = np.pi-math.atan(((2*Eg)+a)/C)+math.atan(((-2*Eg)+a)/C)
    return fractions * brackets
def third_function(A, Eo, C, E, g, a, Eg):
    fraction = 2*((A*Eo*C)/(np.pi*chi(E, g, a, C)))
    brackets = ((Eg*((E**2)-(g**2)))*(np.pi+2*np.arctan(((g**2)-(Eg**2))/(a*C))))
    return fraction * brackets
def fourth_function(A, Eo, C, E, Eg, g, a):
    fractions = (2*(A*Eo*C/(np.pi*chi(E, g, a, C)))*(((E**2)+(Eg**2))/E))
    logarithm = np.log((abs(E-Eg))/(E+Eg))
    return fractions * logarithm
def fifth_function(A, Eo, C, Eg, E, g, a):
    fraction = (2*Eg*(A*Eo*C/(np.pi*chi(E, g, a, C))))
    logarithm = np.log((abs(E-Eg)*(E+Eg))/np.sqrt((((Eo**2)-(Eg**2))**2)+((Eg**2)*(C**2))))
    return fraction*logarithm
def function(Einf, A, C, Eo, Eg, E, a, g):
    first_part = first_function(Eo, Eg, a, A, C, E, g)
    second_part = second_function(A, Eo, Eg, a, C, E, g)
    third_part = third_function(A, Eo, C, E, g, a, Eg)
    fourth_part = fourth_function(A, Eo, C, E, Eg, g, a)
    fifth_part = fifth_function(A, Eo, C, Eg, E, g, a)
    result = Einf + first_part - second_part + third_part - fourth_part + fifth_part
    return result

epsilon = [function(Einf, Amp, Br, Eo, Eg, e, alpha, gamma) for e in eV_range]
complex_permittivity = [complex(t, e) for t, e in zip(epsilon, tauc)]
eps_real = [e.real for e in complex_permittivity]
eps_imag = [e.imag for e in complex_permittivity]
n = [
    np.sqrt((np.sqrt(eps_r ** 2 + eps_i ** 2) + eps_r) / 2)
    for eps_r, eps_i
    in zip(eps_real, eps_imag)]
k = [
    np.sqrt((np.sqrt(eps_r ** 2 + eps_i ** 2) - eps_r) / 2)
    for eps_r, eps_i
    in zip(eps_real, eps_imag)]

fig, ax = plt.subplots(1)
ax.plot(eV_range, k, label='k')
ax.plot(eV_range, n, label='n')
#ax.plot(wavelength_range, eps_real, label='real')
#ax.plot(wavelength_range, eps_imag, label='imag')
ax.legend(loc=0)
plt.show()
