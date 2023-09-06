import matplotlib.pyplot as plt


def spectrumplt(wavelength,
                intensity,
                out_path):
    fig, ax = plt.subplots(
        1,
        figsize=[round(7.5 * 0.393701, 2), round(9 * 0.393701, 2)],
        dpi=600)
    ax.plot(
        wavelength,
        intensity,
        'b',
        lw=2,
        label='Data')
    ax.legend(
        frameon=True,
        loc=0,
        prop={'size': 10})
    ax.set_xlabel(
        'Wavelength [nm]',
        fontsize=15,
        fontweight='bold')
    ax.set_ylabel(
        'Intensity [au]',
        fontsize=15,
        fontweight='bold')
    ax.tick_params(
        axis='both',
        colors='black',
        labelsize=10)
    ax.set_ylim(0, 1)
    plt.savefig(out_path, bbox_inches='tight')
    fig.clf()
    plt.cla()
    plt.close(fig)


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
        1,
        figsize=[round(7.5 * 0.393701, 2), round(9 * 0.393701, 2)],
        dpi=600)
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
        prop={'size': 10})
    ax.set_xlabel(
        'Wavelength [nm]',
        fontsize=15,
        fontweight='bold')
    ax.set_ylabel(
        'Intensity [au]',
        fontsize=15,
        fontweight='bold')
    ax.tick_params(
        axis='both',
        colors='black',
        labelsize=10)
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
    plt.savefig(out_path, bbox_inches='tight')
    fig.clf()
    plt.cla()
    plt.close(fig)