import matplotlib.pyplot as plt

from matplotlib.ticker import AutoMinorLocator


def cm_to_inches(cm: float) -> float:
    """
    Returns centimeters as inches.

    Uses the conversion rate to convert a value given in centimeters to inches.
    Useful for matplotlib plotting.

    Parameters
    ----------
    cm : float
        Value of the desired figure size in centimeters.

    Returns
    -------
    inches : float
        Value of the desired figure size in inches.

    See Also
    --------
    None

    Notes
    -----
    Conversion rate given to 6 decimal places, but inches rounded to 2 decimal
    places.

    Examples
    --------
    >>> cm = 15
    >>> inches = cm_to_inches(cm=cm)
    >>> inches
    5.91

    """
    return round(cm * 0.393701, 2)


def reflectometer_plots(x : list,
                        y1 : list,
                        y2 : list,
                        y1_label : str,
                        y2_label : str,
                        x_axis_label : str,
                        y_axis_label : str,
                        title : str,
                        out_path : str,
                        plot_dict : dict) -> None:
    """
    Plot two y axes against the same x axis.

    Plot wavelength, n, k, or wavelength, eps_r, eps_i, or frequency instead of
    wavelength for the reflectometer.

    Parameters
    ----------
    x, y1, y2: list
        x data, y data for axis 1, y data for axis 2, respectively, as a list.
    x_axis_label, y1_axis_label, y2_axis_label, y1_label, y2_label, title,
    out_path: string
        x axis label, y axis labels, y1 and y2 legend label, graph title, path
        to save.
    plot_dict: dictionary
        Plot settings dictionary, containing:
            {
                "width": plot width,\n
                "height": plot height,\n
                "dpi": dots per square inch,\n
                "grid": True/False,\n
                "legend_loc": legend location,\n
                "legend_col": legend column number,\n
                "legend_size": size of legend text,\n
                "axis_fontsize": font size for axis labels,\n
                "label_size": size for tick labels
            }
    
    Returns
    -------
    None

    See Also
    --------
    matplotlib library

    Notes
    -----
    Plots a standard 2 y-axis graph for the same x data array ideal for the n, k
    and epr_r, eps_i data available from spectroscopic ellipsometry or
    reflectometry.

    Example
    -------
    None

    """
    fig, ax = plt.subplots(
        nrows=1,
        ncols=1,
        figsize=[
            cm_to_inches(cm=plot_dict["width"]),
            cm_to_inches(cm=plot_dict["height"])],
        dpi=plot_dict["dpi"])
    if plot_dict["line"] == "True":
        line1 = ax.plot(
            x,
            y1,
            'blue',
            lw=2,
            label=y1_label)
        line2 = ax.plot(
            x,
            y2,
            'red',
            lw=2,
            label=y2_label)
    else:
        line1 = ax.plot(
            x,
            y1,
            'blue',
            markersize=4,
            label=y1_label)
        line2 = ax.plot(
            x,
            y2,
            'red',
            markersize=4,
            label=y2_label)
    lines = line1 + line2
    labels = [line.get_label() for line in lines]
    if plot_dict["grid"] == "True":
        grid = True
    else:
        grid = False
    ax.grid(
        visible=grid,
        alpha=0.5)
    ax.legend(
        lines,
        labels,
        frameon=True,
        loc=plot_dict["legend_loc"],
        ncol=plot_dict["legend_col"],
        prop={"size": plot_dict["legend_size"]})
    ax.set_xlabel(
        x_axis_label,
        fontsize=plot_dict["axis_fontsize"],
        fontweight='bold')
    ax.set_ylabel(
        y_axis_label,
        fontsize=plot_dict["axis_fontsize"],
        fontweight='bold')
    ax.set_title(
        title,
        fontsize=plot_dict["title_fontsize"],
        fontweight='bold')
    ax.tick_params(
        axis='both',
        which='major',
        labelsize=plot_dict["label_size"])
    ax.xaxis.set_minor_locator(AutoMinorLocator())
    ax.yaxis.set_minor_locator(AutoMinorLocator())
    plt.savefig(
        out_path,
        bbox_inches='tight')
    fig.clf()
    plt.cla()
    plt.close(fig)


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