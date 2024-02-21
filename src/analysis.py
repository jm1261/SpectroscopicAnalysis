import numpy as np
import scipy.optimize as opt
import scipy.constants as const

from src.plotting import fanofitplot
from src.userinput import trimindices


def timecorrected_intensity(raw_intensity,
                            integration_time):
    '''
    Correct raw intensity by multiplying by integration time.
    Args:
        raw_intensity: <array> raw spectrum intensity
        integration_time: <float> integration time in seconds
    Return:
        intensity: <array> time corrected intensity array
    '''
    intensity = [raw / integration_time for raw in raw_intensity]
    return intensity


def normalise_intensity(raw_intensity):
    '''
    Normalise intensity to maximum value in the scan intensity.
    Args:
        raw_intensity: <array> raw scan intensity
    Returns:
        normalised_intensity: <array> normalised intensity array
    '''
    max_intensity = max(raw_intensity)
    normalised_intensity = [
        intensity / max_intensity
        for intensity in raw_intensity]
    return normalised_intensity


def bg_normal_intensity(intensity,
                        background_intensity,
                        integration_time,
                        background_integration_time):
    '''
    Background normalise spectrum to light source.
    Args:
        intensity: <array> spectrum intensity
        background_intensity: <array> background spectrum intensity
        integration_time: <float> spectrum integration time
        background_integration_time: <float> background spectrum integration
                                    time
    Returns:
        normal_intensity: <array> background normalised intensity
    '''
    integration_factor = integration_time / background_integration_time
    normal_intensity = (
        intensity / (integration_factor * background_intensity))
    return normal_intensity


def fano_resonance(x, x0, gamma, q, amplitude, damping):
    '''
    Fano resonance peak equation.
    Args:
        x: <array> x-axis point, wavelength in nm
        x0: <float> peak x point, wavelength in nm
        gamma: <float> reduced frequency
        q: <float> shape factor
        amplitude: <float> peak amplitude
        damping: <float> damping factor
    Returns:
        y: <array> data array for fano peak
    '''
    omega = 2 * ((x - x0) / gamma)
    numerator = ((q + omega) ** 2) + damping
    denominator = 1 + (omega ** 2)
    y = amplitude * (numerator / denominator)
    return y


def get_fano_parameters(wavelength,
                        intensity,
                        sample_name,
                        plot_figure,
                        out_path=False):
    '''
    Use scipy optimise and fano_resonance to iterate and find the peak in
    intensity and the corresponding wavelength and error value.
    Args:
        wavelength: <array> wavelength array in nm
        intensity: <array> intensity array
        sample_name: <string> secondary sample identifier string
        plot_figure: <string> if "True" will plot normalised spectrum with fano
        out_path: <string> path to save, False by default
    Returns:
        peak_wavelength: <dict> dictionary containing:
            popt: <array> fano fit parameters:
                peak, gamma, q, amplitude, damping
            pcov: <array> fano fit errors
                peak, gamma, q, amplitude, damping
    '''
    initial_guesses = [wavelength[np.argmax(intensity)], 10, 5, 0.6, 1]
    try:
        popt, pcov = opt.curve_fit(
            fano_resonance,
            wavelength,
            intensity,
            initial_guesses)
        errors = np.sqrt(np.diag(pcov))
    except RuntimeError:
        print('\nRun Time Error \nNo Peak Found')
        popt = [0, 0, 0, 0, 0]
        errors = [0, 0, 0, 0, 0]
    peak_wavelength = popt[0]
    peak_wavelength_error = errors[0]
    if plot_figure == 'True':
        fanofitplot(
            wavelength=wavelength,
            intensity=intensity,
            fano=[
                fano_resonance(
                    x=wav,
                    x0=popt[0],
                    gamma=popt[1],
                    q=popt[2],
                    amplitude=popt[3],
                    damping=popt[4])
                for wav in wavelength],
            peak_wavelength=peak_wavelength,
            peak_error=peak_wavelength_error,
            out_path=out_path)
    return {
        f'{sample_name} Fano Fit Parameters': [
            'Peak', 'Gamma', 'q', 'Ampltidude', 'Damping'],
        f'{sample_name} Fano Fit': [value for value in popt],
        f'{sample_name} Fano Errors': [value for value in errors],
        f'{sample_name} Wavelength': [w for w in wavelength],
        f'{sample_name} Intensity': [i for i in intensity]}


def get_peak_wavelength(fano_parameters,
                        sample_name):
    '''
    Get peak wavelength from fano fit parameters.
    Args:
        fano_parameters: <dict> dictionary containing Fano Fit and Fano Fit
                            Errors
        sample_name: <string> secondary sample identifier string
    Returns:
        peak_wavelength: <dict>
            Peak Wavelength (nm)
            Peak Error (nm)
    '''
    peak_wavelength = (fano_parameters[f'{sample_name} Fano Fit'])[0]
    peak_error = (fano_parameters[f'{sample_name} Fano Errors'])[1]
    return {
        f'{sample_name} Peak Wavelength': peak_wavelength,
        f'{sample_name} Peak Error': peak_error}


def calc_peakwavelength(wavelength,
                        normalised_intensity,
                        sample_details,
                        plot_figure,
                        out_path=False):
    '''
    Calculate peak wavelength of normalised intensity from spectrometer scan.
    Trim file to region of interest and use fano-peak resonance function to find
    peak wavelength.
    Args:
        wavelength: <array> wavelength array
        normalised_intensity: <array> normalised intensity array
        sample_details: <dict> sample details dictionary
        plot_figure: <string> if "True" plots the peak figure
        out_path: <string> path to save file, default False
    Returns:
        results_dictionary: <dict>
            Region Trim Index: <array> min, max indices
            popt: <array> fano fit parameters:
                peak, gamma, q, amplitude, damping
            pcov: <array> fano fit errors
                peak, gamma, q, amplitude, damping
            Peak Wavelength (nm)
            Peak Error (nm)
    '''
    parent = sample_details['Parent Directory']
    region_string = sample_details[f'{parent} Secondary String']
    trim_indices = trimindices(
        x_array=wavelength,
        y_array=normalised_intensity,
        file_name=sample_details[f'{parent} File Name'],
        region=region_string,
        y_limit=(0, 1))
    fano_parameters = get_fano_parameters(
        wavelength=wavelength[
            (trim_indices[f'{region_string} Trim Index'])[0]:
            (trim_indices[f'{region_string} Trim Index'])[1]],
        intensity=normalised_intensity[
            (trim_indices[f'{region_string} Trim Index'])[0]:
            (trim_indices[f'{region_string} Trim Index'])[1]],
        sample_name=sample_details[f'{parent} Secondary String'],
        plot_figure=plot_figure,
        out_path=out_path)
    peak_wavelength = get_peak_wavelength(
        fano_parameters=fano_parameters,
        sample_name=sample_details[f'{parent} Secondary String'])
    results_dictionary = dict(
        trim_indices,
        **fano_parameters,
        **peak_wavelength)
    return results_dictionary


def cauchy_fits(wavelength : list,
                model : dict) -> list:
    """
    Calculate the Cauchy model refractive index and extinction coefficient.

    Parameters
    ----------
    wavelength: list
        List of wavelengths at which to analyse the refractive index and
        extinction coefficient.
    model: dictionary
        Fit model containing the A, B, and C components of the cauchy model.

    Returns
    -------
    n, k: list
        Refractive index and extinction coefficient values over the specified
        wavelength range.

    See Also
    --------
    None

    Notes
    -----
    The Cauchy model is used to describe the wavelength dependent refractive
    index of a material using at least three parameters (A, B, and C). It
    can be extended to an imaginary component, but this is an approximation.

    Example
    -------
    None

    """
    wavelength_um = [x / 1E3 for x in wavelength]
    n = [
        (model["A"])[0] +
        ((model["B"])[0] / (x ** 2)) +
        ((model["C"])[0] / (x ** 4))
        for x in wavelength_um]
    k = [
        a * np.tan(np.arctan2(np.imag(a), np.real(a)))
        for a in n]
    return n, k


def epsilon(refractive_index : list,
            extinction_coefficient : list) -> list:
    """
    Calculate the real and imaginary components of the permittivity from n, k.

    Parameters
    ----------
    refractive_index, extinction_coefficient: list
        n and k values at which to calculate the permittivity.

    Returns
    -------
    eps_real, eps_imag: list
        Real and imaginary components of the permittivity.

    See Also
    --------
    cauchy_fits

    Notes
    -----
    This is a simplistic calculation for epsilon based on the complex refractive
    index equation.

    Example
    -------
    None

    """
    eps_real = [
        (a ** 2) - (b ** 2)
        for a, b
        in zip(refractive_index, extinction_coefficient)]
    eps_imag = [
        2 * a * b
        for a, b
        in zip(refractive_index, extinction_coefficient)]
    return eps_real, eps_imag


def cody_lorentz_oscillator(amplitude : float,
                            oscillator_energy : float,
                            broadening : float,
                            omega : float) -> complex:
    """
    Calculate the permittivity at a specified angular frequency for a
    Cody-Lorentz oscillator.

    Parameters
    ----------
    amplitude, oscillator_energy, broadening, omega: float
        Cody-Lorentz oscillator amplitude, energy, broadening parameter, and the
        angular frequency at which to evaluate the model.

    Returns
    -------
    epsilon: complex
        Complex permittivity at specified angular frequency.

    See Also
    --------
    None

    Notes
    -----
    The Cody-Lorentz model is a modification of the Lorentz oscillator model
    that incorporates an additional term to account for the dispersion of the
    refractive index. This model does not include a Drude component or the high
    frequency permittivity.

    Example
    -------
    None

    """
    epsilon = (
        (amplitude * oscillator_energy) /
        (complex(
            (oscillator_energy ** 2) - (omega ** 2), -(omega * broadening))))
    return epsilon


def drudeoscillator(scattering_time : float,
                    plasma_frequency : float,
                    omega: float) -> complex:
    """
    Calculate the permittivity at a specified angular frequency for a Drude
    oscillator.

    Parameters
    ----------
    scattering_time, plasma_frequency, omega: float
        The scattering time, plasma frequency, and angular frequency at which
        to evaluate the permittivity. Note that plasma frequency is not squared
        as the input argument.

    Returns
    -------
    epsilon: complex
        Complex permittivity at specified angular frequency.

    See Also
    --------
    None

    Notes
    -----
    The Drude model is a classical model that describes the behaviour of free
    electrons in a metal when subjected to an external electromagnetic field,
    assuming that electrons in the material behave like a classical gas,
    experiencing collisions with the lattice ions.

    Example
    -------
    None

    """
    if scattering_time == 0:
        gamma = 0
    else:
        gamma = 1 / scattering_time
    epsilon = (plasma_frequency ** 2) / (omega * complex(omega, gamma))
    return epsilon


def graded_material(wavelength : list,
                    model : dict) -> list:
    """
    Calculate the real and imaginary components of the complex permittivity as
    given by the cody lorentz model.

    Parameters
    ----------
    wavelength: list
        Wavelength range at which to analyse the complex permittivity.
    model: dictionary
        Fit model containing the cody lorentz model components.

    Returns
    -------
    eps_real, eps_imag: list
        Real and imaginary components of the permittivity.

    See Also
    --------
    None

    Notes
    -----
    The Cody-Lorentz model is used to describe the complex permittivity of a
    material that exhibits Lorentz oscillator and Drude oscillator behaviour.

    Example
    -------
    None

    """
    frequency = [3E8 / (w * 1E-9) for w in wavelength]
    omega = [2 * np.pi * f for f in frequency]
    cody_components = model['e1 Components']
    lorentz_components = (model['e2 Components'])['Harmonic']
    drude_components = (model['e2 Components'])['Drude']
    Einf = (cody_components["Einf"])[0]
    lorentz_oscillator = [
        cody_lorentz_oscillator(
            amplitude=(lorentz_components["Amp1"])[0],
            oscillator_energy=(lorentz_components["En1"])[0],
            broadening=(lorentz_components["Br1"])[0],
            omega=w)
        for w in omega]
    rho = (drude_components["Resistivity"])[0]
    mu = (drude_components["Mobility"])[0]
    m_star = (drude_components["M*"])[0]
    plasma_frequency = np.sqrt(
        1.602E-19 / (rho * mu * 8.85E-12 * 9.109E-31 * m_star))
    drude_oscillator = [
        drudeoscillator(
            scattering_time=(drude_components["Scattering"])[0],
            plasma_frequency=plasma_frequency,
            omega=w)
        for w in omega]
    epsilon_complex = [
        Einf - lorentz - drude
        for lorentz, drude
        in zip(lorentz_oscillator, drude_oscillator)]
    eps_real = [eps.real for eps in epsilon_complex]
    eps_imag = [abs(eps.imag) for eps in epsilon_complex]
    return eps_real, eps_imag


def parameterised_materials(wavelength : list,
                            model : dict) -> list:
    """
    """
    frequency = [3E8 / (w * 1E-9) for w in wavelength]
    omega = [2 * np.pi * f for f in frequency]
    cody_components = model['e1 Components']
    lorentz_components = (model['e2 Components'])['Cody-Lorentz']
    Einf = (cody_components["Einf"])[0]
    lorentz_oscillator = [
        cody_lorentz_oscillator(
            amplitude=(lorentz_components["Amp1"])[0],
            oscillator_energy=(lorentz_components["Eo1"])[0],
            broadening=(lorentz_components["Br1"])[0],
            omega=w)
        for w in omega]
    Eg = (lorentz_components["Eg1"])[0]
    plasma_frequency = (Eg * 1.6E-19 / const.hbar)
    drude_oscillator = [
        drudeoscillator(
            scattering_time=0,
            plasma_frequency=plasma_frequency,
            omega=w)
        for w in omega]
    epsilon_complex = lorentz_oscillator
    eps_real = [eps.real for eps in epsilon_complex]
    eps_imag = [abs(eps.imag) for eps in epsilon_complex]
    return eps_real, eps_imag


def comp_RI(epsilon_real : list,
            epsilon_imaginary : list) -> list:
    """
    Calculate the refractive index and extinction coefficient parameters from
    the complex permittivity.

    Parameters
    ----------
    epsilon_real, epsilon_imaginary: list
        Real and imaginary components of the permittivity.

    Returns
    -------
    n, k: list
        Real and imaginary components of the complex refractive index.

    See Also
    --------
    epsilon

    Notes
    -----
    The real and imaginary components of the refractive index, n and k, can be
    calculated from the complex permittivity according to standard equations.

    Example
    -------
    None

    """
    n = [
        np.sqrt((np.sqrt(eps_r ** 2 + eps_i ** 2) + eps_r) / 2)
        for eps_r, eps_i
        in zip(epsilon_real, epsilon_imaginary)]
    k = [
        np.sqrt((np.sqrt(eps_r ** 2 + eps_i ** 2) - eps_r) / 2)
        for eps_r, eps_i
        in zip(epsilon_real, epsilon_imaginary)]
    return n, k
