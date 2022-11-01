import numpy as np
import scipy.optimize as opt
from src.plotting import fanofitplot
from numpy.random import rand


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


def background_subtract(background_intensity,
                        intensity):
    '''
    Remove background intensity from scan intensity.
    Args:
        background_intensity: <array> background spectrum intensity
        intensity: <array> spectrum intensity
    Return:
        background_subtract_intensity: <array> normalised intensity
    '''
    background_subtract_intensity = [
        scan_int - bg_int
        for bg_int, scan_int
        in zip(background_intensity, intensity)]
    return background_subtract_intensity


def normalised_intensity(intensity):
    '''
    Normalise intensity to maximum intensity value in intensity.
    Args:
        intensity: <array> spectrum intensity
    Returns:
        normalised_intensity: <array> normalised intensity array
    '''
    max_intensity = max(intensity)
    normalised_intensity = [scan_int / max_intensity for scan_int in intensity]
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
    delta = 2 * ((x - x0) / gamma)
    numerator = ((q + delta) ** 2) + damping
    denominator = 1 + (delta ** 2)
    y = amplitude * (numerator / denominator)
    return y


def findpeak_wavelength(wavelength,
                        intensity,
                        plot=False,
                        out_path=False):
    '''
    Use scipy optimise and fano_resonance to iterate and find the peak in
    intensity and the corresponding wavelength and error value.
    Args:
        wavelength: <array> wavelength array in nm
        intensity: <array> intensity array
    Returns:
        peak_wavelength: <dict> dictionary containing:
            popt: <array> fano fit parameters:
                peak, gamma, q, amplitude, damping
            pcov: <array> fano fit errors
                peak, gamma, q, amplitude, damping
    '''
    initial_guesses = [wavelength[np.argmax(intensity)], 50, 5, 0.6, 0]
    sigma = np.ones(len(intensity))
    popt, pcov = opt.curve_fit(
        fano_resonance,
        wavelength,
        intensity,
        initial_guesses,
        sigma)
    errors = np.sqrt(np.diag(pcov))
    print(popt)
    peak_wavelength = popt[0]
    peak_wavelength_error = errors[0]
    if plot:
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
        "Fano Fit Parameters": ['Peak', 'Gamma', 'q', 'Ampltidude', 'Damping'],
        "Fano Fit": [value for value in popt],
        "Fano Errors": [value for value in errors]}
