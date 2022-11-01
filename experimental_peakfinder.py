import os
import src.fileIO as io
import src.filepaths as fp
import src.userinput as ui
import src.analysis as anal


if __name__ == '__main__':

    ''' Organisation '''
    root = os.getcwd()
    GMRX_files, background_path, results_path = fp.get_filepaths(root_path=root)

    ''' Loop Files '''
    for file in GMRX_files:

        ''' Load files and sample details '''
        wavelength, raw_intensity = io.read_GMRX_file(file_path=file)
        sample_parameters = fp.sample_parameters(
            file_name=fp.get_filename(
                file_path=file))

        ''' Region of Interest '''
        trim_index = ui.trimindices(
            x_array=wavelength,
            y_array=raw_intensity,
            file_name=sample_parameters['File Name'])

        ''' Background Correction '''
        try:
            background_file = fp.find_background(
                background_path=background_path,
                sample_name=sample_parameters['Sample Name'],
                polarisation=sample_parameters['Polarisation'])
        except:
            background_file = []

        if len(background_file) == 0:
            normalised_intensity = anal.normalised_intensity(
                intensity=anal.timecorrected_intensity(
                    raw_intensity=raw_intensity,
                    integration_time=sample_parameters['Integration Time']))
            bg_parameters = {"BG String": "No BG File"}

        else:
            _, bg_raw_intensity = io.read_GMRX_file(
                file_path=background_file)
            bg_parameters = fp.background_parameters(
                file_name=fp.get_filename(
                    file_path=background_file))
            normalised_intensity = anal.bg_normal_intensity(
                intensity=raw_intensity,
                background_intensity=bg_raw_intensity,
                integration_time=sample_parameters['Integration Time'],
                background_integration_time=(
                    bg_parameters['Bg Integration Time']))

        ''' Find Peak Wavelength '''
        peak_wavelength = anal.findpeak_wavelength(
            wavelength=wavelength[
                trim_index['Min Trim Index']: trim_index['Max Trim Index']],
            intensity=normalised_intensity[
                trim_index['Min Trim Index']: trim_index['Max Trim Index']],
            plot=True,
            out_path=os.path.join(
                results_path,
                f'{sample_parameters["File Name"]}.png'))

        ''' Save Out '''
        results_dictionary = dict(
            sample_parameters,
            **bg_parameters,
            **trim_index,
            **peak_wavelength)
        io.save_json_dicts(
            out_path=os.path.join(
                results_path,
                f'{sample_parameters["File Name"]}.json'),
            dictionary=results_dictionary)
