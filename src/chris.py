import numpy as np
import scipy.optimize as opt

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


def fano_resonance(x, amp, assym, res, gamma, off):
    '''
    Chris' fano resonance equation
    '''
    numerator = ((assym * gamma) + (x - res)) * ((assym * gamma) + (x - res))
    denominator = (gamma * gamma) + ((x - res) * (x - res))
    y = (amp * (numerator / denominator)) + off
    return y


def get_fano_parameters(wavelength,
                        intensity,
                        sample_name,
                        plot_figure,
                        out_path=False):
    '''
    Chris' fano parameters
    '''
    initial_peak = wavelength[np.argmax(intensity)]
    initial_guesses = [1, 1, initial_peak, 10, 1]
    bounds = (
        (initial_peak - 25, -10, -2 * np.pi),
        (initial_peak + 25, 10, 2 * np.pi))
    try:
        popt, pcov = opt.curve_fit(
            f=fano_resonance,
            xdata=wavelength,
            ydata=intensity,
            p0=initial_guesses)
        errors = np.sqrt(np.diag(pcov))
    except RuntimeError:
        print('\nRun Time Error \nNo Peak Found')
        popt = [0, 0, 0, 0, 0]
        errors = [0, 0, 0, 0, 0]
    peak_wavelength = popt[2]
    peak_wavelength_error = errors[2]
    if plot_figure == 'True':
        fanofitplot(
            wavelength=wavelength,
            intensity=intensity,
            fano=[
                fano_resonance(
                    x=wav,
                    amp=popt[0],
                    assym=popt[1],
                    res=popt[2],
                    gamma=popt[3],
                    off=popt[4])
                for wav in wavelength],
            peak_wavelength=peak_wavelength,
            peak_error=peak_wavelength_error,
            out_path=out_path)
    return {
        f'{sample_name} Fano Fit Parameters': [
            'amp', 'assym', 'res', 'gamma', 'off'],
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
    peak_wavelength = (fano_parameters[f'{sample_name} Fano Fit'])[2]
    peak_error = (fano_parameters[f'{sample_name} Fano Errors'])[2]
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
