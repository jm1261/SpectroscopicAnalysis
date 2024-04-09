import numpy as np
import matplotlib.pyplot as plt

from matplotlib.widgets import RectangleSelector


def lineselect_callback(eclick,
                        erelease) -> tuple:
    """
    Function Details
    ================
    Callback function for handling click and release events of the
    RectangleSelector.

    Parameters
    ----------
    eclick, erelease: MouseEvent
        The mouse event corresponding to the initial click point and release
        point.

    Returns
    -------
    tuple:
        A tuple containing the x and y coordinates of the bottom left and top
        right corners of the selected region.

    See Also
    --------
    None.

    Notes
    -----
    This function is invoked when a user selects a rectangular region of
    interest on a plot using the RectangleSelector widget. It records the
    coordinates of the click and release events within the selected region.

    Example
    -------
    None

    ----------------------------------------------------------------------------
    Update History
    ==============

    09/04/2024
    ----------
    Documentation update.

    """
    global x1, y1, x2, y2
    x1, y1 = eclick.xdata, eclick.ydata
    x2, y2 = erelease.xdata, erelease.ydata
    print('(%3.2f, %3.2f) --> (%3.2f, %3.2f)' % (x1, y1, x2, y2))
    print('The button you used were: %s %s' % (eclick.button, erelease.button))
    return x1, y1, x2, y2


def toggle_selector(event) -> None:
    """
    Function Details
    ================
    Toggle function for activating/deactivating the RectangleSelector.

    Parameters
    ----------
    event: KeyEvent
        They key event triggered when a key is pressed.

    Returns
    -------
    None

    See Also
    --------
    None.

    Notes
    -----
    This function toggles the activation state of the RectangleSelector based on
    key presses. Pressing 'Q' or 'q' deactivates the selector, while pressing
    'A' or 'a' activates it.

    Example
    -------
    None

    ----------------------------------------------------------------------------
    Update History
    ==============

    09/04/2024
    ----------
    Documentation updated.

    """
    print('Key Pressed')
    if event.key in ['Q', 'q'] and toggle_selector.RS.active:
        print('RectangleSelector Deactivated')
        toggle_selector.RS.set_active(False)
    if event.key in ['A', 'a'] and not toggle_selector.RS.active:
        print('RectangleSelector Activated')
        toggle_selector.RS.set_active(True)


def region_interest(x : list,
                    y : list,
                    file_name : str,
                    y_limit=False) -> tuple:
    """
    Function Details
    ================
    User selected area of interest of a graph.

    Plots xy-graph and allows a rectangle region of interest to be selected.

    Parameters
    ----------
    x, y: list
        x- and y- data arrays.
    file_name: string
        Name of file without extensions.
    y_limit: bool/tuple
        Y limit for plotting, if true must be (ymin, ymax).

    Returns
    -------
    x1, y1, x2, y2: float
        x and y coordinates for the bottom left and bottom right corner of the
        rectangle selector.

    See Also
    --------
    RectangleSelector
    lineselect_callback
    toggle_selector

    Notes
    -----
    Uses matplotlib rectangle selector widget.

    Example
    -------
    None.

    ----------------------------------------------------------------------------
    Update History
    ==============

    09/04/2024
    ----------
    Documentation update. Had to remove drawtype='box' from the code as this is
    no longer in the documentation.

    """
    fig, ax = plt.subplots(
        1,
        figsize=[10, 7])
    ax.plot(
        x,
        y,
        'red',
        lw=2,
        label=file_name)
    ax.legend(
        frameon=True,
        loc=0,
        prop={'size': 14})
    ax.grid(True)
    ax.tick_params(
        axis='both',
        colors='black',
        labelsize=12)
    ax.set_xlabel(
        'x',
        fontsize=14,
        fontweight='bold',
        color='black')
    ax.set_ylabel(
        'y',
        fontsize=14,
        fontweight='bold',
        color='black')
    ax.set_xlim(min(x), max(x))
    if y_limit:
        ax.set_ylim(y_limit)
    print('\n   click  -->  release')
    toggle_selector.RS = RectangleSelector(
        ax,
        lineselect_callback,
        useblit=True,
        button=[1, 3],
        minspanx=5,
        minspany=5,
        spancoords='pixels',
        interactive=True)
    plt.connect(
        'key_press_event',
        toggle_selector)
    plt.show()
    return x1, y1, x2, y2


def trimindices(x_array : list,
                y_array : list,
                file_name : str,
                y_limit=False) -> dict:
    """
    Function Details
    ================
    Trim arrays to region of interest.

    Parameters
    ----------
    x_array, y_array: list
        X- and Y- data arrays.
    file_name: string
        File name for graphing region of interest.
    y_limit: bool/tuple
        y-limit for region of interest plotting, if true must be (ymin, ymax).

    Returns
    -------
    dictionary: dict
        Dictionary containing the region identifier and minimum/maximum region
        indices for the x-data array.
        {(Region) Trim Index: [min_index, max_index]}.

    See Also
    --------
    region_interest
    numpy argmin

    Notes
    -----
    None.

    Example
    -------
    None.

    ----------------------------------------------------------------------------
    Update History
    ==============

    09/04/2024
    ----------
    Documentation update.

    """
    x1, _, x2, _ = region_interest(
        x=x_array,
        y=y_array,
        file_name=file_name,
        y_limit=y_limit)
    min_index = np.argmin(np.abs(x_array - x1))
    max_index = np.argmin(np.abs(x_array - x2))
    return {
        "Spectrum Trim Index": [min_index, max_index]}


if __name__ == '__main__':
    x_data = [1, 2, 3, 4, 5]
    y_data = [1, 2, 3, 4, 5]
    x1, y1, x2, y2 = region_interest(
        x=x_data,
        y=y_data,
        file_name='Test')
