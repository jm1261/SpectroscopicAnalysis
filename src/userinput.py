import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import RectangleSelector


def lineselect_callback(eclick,
                        erelease):
    '''
    Return x and y coordinates of click and release region of interest.
    Args:
        eclick: <float> start coordinates of click
        erelease: <float> end coordinates of click
    Returns:
        x1: <float> xi coordinate of region of interest
        x2: <float> xf coordinate of region of interest
        y1: <float> yi coordinate of region of interest
        y2: <float> yf coordinate of region of interest
    '''
    global x1, y1, x2, y2
    x1, y1 = eclick.xdata, eclick.ydata
    x2, y2 = erelease.xdata, erelease.ydata
    print('(%3.2f, %3.2f) --> (%3.2f, %3.2f)' % (x1, y1, x2, y2))
    print('The button you used were: %s %s' % (eclick.button, erelease.button))
    return x1, y1, x2, y2


def toggle_selector(event):
    '''
    Determines if a key has been pressed.
    Args:
        event: <click> triggered event
    Returns:
        None
    '''
    print('Key Pressed')
    if event.key in ['Q', 'q'] and toggle_selector.RS.active:
        print('RectangleSelector Deactivated')
        toggle_selector.RS.set_active(False)
    if event.key in ['A', 'a'] and not toggle_selector.RS.active:
        print('RectangleSelector Activated')
        toggle_selector.RS.set_active(True)


def region_interest(x, y,
                    file_name):
    '''
    Allows uer to select an area of a graph of interest. Plots an x-y graph and
    uses matplotlib rectangle selector to select region of interest. The x, y
    coordinates for the region are returned.
    Args:
        x: <array> x-axis data array
        y: <array> y-axis data array
        file_name: <string> file identifier for data label
    Returns:
        x1: <float> x coordinate for the start position of region of interest
        y1: <float> y coordinate for the start position of region of interest
        x2: <float> x coordinate for the end position of region of interest
        y2: <float> y coordinate for the end position of region of interest
    '''
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
    print('\n   click  -->  release')
    toggle_selector.RS = RectangleSelector(
        ax,
        lineselect_callback,
        drawtype='box',
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


def trimindices(x_array,
                y_array,
                file_name):
    '''
    Trim arrays to region of interest, return the array min/max indices.
    Args:
        x_array: <array> x-axis data
        y_array: <array> y-axis data
        file_name: <string> file indentifier for data label
    Returns:
        index: <dict> dictionary containing:
            min_index: <int> minimum index in full array for region of interest
            max_index: <int> maximum index in full array for region of interest
    '''
    x1, _, x2, _ = region_interest(
        x=x_array,
        y=y_array,
        file_name=file_name)
    min_index = np.argmin(np.abs(x_array - x1))
    max_index = np.argmin(np.abs(x_array - x2))
    return {
        "Min Trim Index": min_index,
        "Max Trim Index": max_index}
