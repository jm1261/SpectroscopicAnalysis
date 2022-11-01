import matplotlib.pyplot as plt


def fanofitplot(wavelength,
                intensity,
                fano,
                out_path,
                peak_wavelength,
                peak_error,
                show=False):
    '''
    Plot wavelength, intensity, and fano peak fit on same axis.
    Args:
        wavelength: <array> wavelength array
        intensity: <array> intensity array
        fano: <array> fano fit intensity array
        out_path: <string> path to save
        peak_wavelength: <string> calculated peak wavelength
        peak_error: <string> calculated peak wavelength error
        show: <bool> if True, plot shows, always saves
    Returns:
        None
    '''
    fig, ax = plt.subplots(
        nrows=1,
        ncols=1,
        figsize=[10, 7])
    ax.plot(
        wavelength,
        intensity,
        'b',
        lw=2,
        label='Data')
    ax.plot(
        wavelength,
        fano,
        'r',
        lw=2,
        label='Fano Fit')
    ax.legend(
        frameon=True,
        loc=0,
        prop={'size': 14})
    ax.set_xlabel(
        'Wavelength [nm]',
        fontsize=14,
        fontweight='bold')
    ax.set_ylabel(
        'Intensity [au]',
        fontsize=14,
        fontweight='bold')
    ax.tick_params(
        axis='both',
        colors='black',
        labelsize=14)
    text_string = (
        f'Peak = ({round(peak_wavelength, 2)} +/- {round(peak_error, 2)})nm')
    props = dict(
        boxstyle='round',
        facecolor='wheat',
        alpha=0.5)
    ax.text(
        0.05,
        0.05,
        text_string,
        transform=ax.transAxes,
        verticalalignment='top',
        bbox=props)
    if show:
        plt.show()
    plt.savefig(out_path)
    fig.clf()
    plt.cla()
    plt.close(fig)