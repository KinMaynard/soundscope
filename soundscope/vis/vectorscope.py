import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.widgets import RadioButtons
import matplotlib.gridspec as gridspec
import mpl_toolkits.axisartist.floating_axes as floating_axes


# Use backend that supports animation, blitting & figure window resizing
mpl.use('Qt5Agg')

# Ignore divide by 0 error in log
np.seterr(divide='ignore')


def vectorscope(array, name, channels, sample_rate, fig=None, sub=False, 
                gridspec=None, resize_ls=None):
    """
    A stereo vectorscope plot of audio data.

    Plot in either polar dot per sample or lissajous modes Left/Right
    amplitudes as coordinates on X/Y 180 degree polar plot or coordinate
    plane lissajous plot. Currently only lissajous mode active.

    Lissajous vectorscope dot per sample plotting stereo width of the
    audio signal.
    Mono signals show as straight lines down the center, stereo
    information is show with horizontal deflection of the data.
    Phase issues show as extreme horizontal deflection with full out of
    phase signals showing as horizontal line.

    The Polar/Lissajous radio button chooses which plot to show.
    Polar plot currently unavailable.

    array: array of audio data
    name: audio datafile name
    channels: 1 mono or 2 stereo, number of channels in audio array
    sample_rate: sampling rate of audio file
    fig: external figure to plot onto if provided, default = None
    sub: boolean, True: plotting as subplot of larger figure, False:
    otherwise, default False
    gridspec: gridspec to plot onto if part of a larger figure
    otherwise None, default None
    resize_ls: list of text objects to be resized on window resize
        events when plotting inside visualizer, default None

    returns: a vectorscope polar dot per sample plot of audio data
    or a lissajouse dot per sample vectorscope plot of the audio array
    """

    # Dark background white text
    plt.style.use('dark_background')

    # Setting font
    mpl.rcParams['font.family'] = 'sans-serif'
    mpl.rcParams['font.sans-serif'] = 'Helvetica'
    # mpl.rcParams['agg.path.chunksize'] = 20000

    # Setting axis limits to data peaks
    hi_bound = np.max(np.absolute(array))
    low_bound = np.negative(hi_bound)
    extents = low_bound, hi_bound, low_bound, hi_bound

    # Making floating axes and rotating it 45 degrees
    transform = mpl.transforms.Affine2D().rotate_deg(45)
    helper = floating_axes.GridHelperCurveLinear(transform, extents)

    # Initilize polar & lissajous figure and axes for solo plot
    if fig is None:
        fig, pol_ax = plt.subplots(subplot_kw={'projection': 'polar'})
        float_ax = fig.add_subplot(axes_class=floating_axes.FloatingAxes,
                                   grid_helper=helper)
        # phase_ax = fig.add_subplot() #polar=True

    # Polar & lissajous figure + axes for subplotting inside visualizer
    else:
        if channels == '1':
            pol_ax = fig.add_subplot(224, polar=True)
            float_ax = fig.add_subplot(224,
                                       axes_class=floating_axes.FloatingAxes,
                                       grid_helper=helper)
            # phase_ax = fig.add_subplot(224)

        else:
            pol_ax = fig.add_subplot(gridspec[0, 1], polar=True)
            float_ax = fig.add_subplot(gridspec[0, 1],
                                       axes_class=floating_axes.FloatingAxes,
                                       grid_helper=helper)
            # phase_ax = fig.add_subplot(gridspec[0, 1])

    # Phase spectrum plot
    # Set phase spectrum title
    # phase_ax.set_title('Phase Spectrum', color='#F9A438', fontsize=10)

    # Plotting phase spectrum
    # spectrum, freqs, line = phase_ax.phase_spectrum(array, Fs=sample_rate)
    # spectrum, freqs, line = phase_ax.angle_spectrum(array, Fs=sample_rate)

    # Double up mono signals to display them
    if channels == '1':
        array = .5 * array
        array = np.stack((array, array), axis=-1)

    # Plotting coherence
    # Cxy, freqs = phase_ax.cohere(array[:,1], array[:,0], NFFT=128,
                                  #Fs=sample_rate)

    # Turn off tick labels, ticks & axis labels
    float_ax.axis['top', 'bottom', 'left', 'right'].toggle(all=False)

    # Setting spine color
    float_ax.axis['top', 'bottom', 'left', 'right'].line.set_color('#F9A438')

    # Diagonal spine right
    float_ax.axline((-1, -1), (1, 1), color='#F9A438', lw=1, zorder=3)

    # Diagonal spine left
    float_ax.axline((-1, 1), (1, -1), color='#F9A438', lw=1, zorder=3)

    # Setting the title of the plot
    title = '%s LISSAJOUS VECTORSCOPE' % name
    if sub:
        title = 'LISSAJOUS VECTORSCOPE'
        if channels == '1':
            float_title = float_ax.set_title(title, y=0.78, color='#F9A438',
                                            fontsize=10, pad=80)
        else:
            float_title = float_ax.set_title(title, y=.78, color='#F9A438',
                                             fontsize=10, pad=55)
    else:
        float_title = float_ax.set_title(title, color='#F9A438', fontsize=10)

    # Base transformation of data
    base = plt.gca().transData
    rot = mpl.transforms.Affine2D().rotate_deg(45)

    # Add annotations for quadrants (axis labels)
    l_pos = float_ax.text(0.22, .76, '+L', color='#F9A438', fontsize=7,
                          transform=float_ax.transAxes)
    l_neg = float_ax.text(.75, 0.225, '-L', color='#F9A438', fontsize=7,
                          transform=float_ax.transAxes)
    r_pos = float_ax.text(.75, .75, '+R', color='#F9A438', fontsize=7,
                          transform=float_ax.transAxes)
    r_neg = float_ax.text(0.22, 0.225, '-R', color='#F9A438', fontsize=7,
                          transform=float_ax.transAxes)

    # Making lissajous lines (doesn't work)
    # x = array[:,1] * np.sin(np.fft.fft(array[:,1]) * (array.size
                                                      # / sample_rate))
    # y = array[:,0] * np.sin(np.fft.fft(array[:,0]) * (array.size
                                                      # / sample_rate))

    # Plotting data
    float_ax.plot(array[:,1], array[:,0], 'o', color='#4B9D39',
                  markersize=0.05, transform=rot + base)

    # Lissajous curve plotting
    # float_ax.plot(x, y, color='#4B9D39', markersize=0.05,
                  # transform=rot + base)

    # Initially hide lissajous vectorscope
    # float_ax.set_visible(False)

    # New transform attempt
    mask = array < 0
    mask2 = np.stack((mask[:,0] == mask[:,1], mask[:,0] == mask[:,1]), axis=1)
    array = np.where(mask2, np.absolute(array), np.negative(array))
    left, right = np.split(array, 2, axis=1)
    r = left
    theta = right

    # Plotting
    plot = pol_ax.plot(theta, r, 'o', color='#4B9D39', markersize=0.05)

    # Set title & bring down close to top of plot
    title = '%s POLAR DOT PER SAMPLE VECTORSCOPE' % name
    if sub:
        title = 'POLAR DOT PER SAMPLE VECTORSCOPE'
        if channels == '1':
            title_vec = pol_ax.set_title(title, y=0.78, color='#F9A438',
                                         fontsize=10)
        else:
            title_vec = pol_ax.set_title(title, y=.78, color='#F9A438',
                                         fontsize=10)
    else:
        title_vec = pol_ax.set_title(title, color='#F9A438', fontsize='medium',
                                     pad=-60)

    # Plotting 180 degrees
    pol_ax.set_thetamax(180)

    # Setting the outer grid max to the max of the array
    peak = np.amax(array)
    pol_ax.set_rmax(peak)

    # Removing y axis labels and most grids
    pol_ax.set_yticklabels([])
    pol_ax.grid(False, axis='y')

    # Setting spine color, no api for the bottom spines so need to use
    # get_children
    artists = pol_ax.get_children()
    pol_spines = [i for i in artists[1:4]]
    for s in pol_spines:
        s.set_color('#F9A438')

    # Plotting only 2 theta grids
    theta_lines, theta_labels = pol_ax.set_thetagrids((135.0, 90.0, 45.0),
                                                      labels=('L', 'C', 'R'),
                                                      color='#F9A438',
                                                      fontsize=7)

    # Thetagrid color
    pol_ax.xaxis.grid(color='#F9A438')

    # Compensating for partial polar plot extra whitespace:
    # Left, bottom, width, height
    if not sub:
        pol_ax.set_position([0.1, 0.05, 0.8, 1])

    else:
        if channels == '1':
            # Left, bottom, width, height
            pol_ax.set_position([0.55, -0.735, 0.350, 2.023])

        else:
            pol_ax.set_position([0.6, -0.772, 0.245, 2])

    # Hide polar vectorscope
    pol_ax.set_visible(False)

    # Polarlissa button axis.
    # Solo plot
    if not sub:
        # Left, bottom, width, height
        rax = plt.axes([0.05, 0.7, 0.13, 0.1], facecolor='black',
                       frame_on=False)

    # Part of visualizer
    else:
        rax = plt.axes([0.71, 0.05, 0.06, 0.045], facecolor='black',
                       frame_on=False)

    # Polarlissa radio button
    polarlissa = RadioButtons(rax, ('Polar', 'Lissajous'),
                              activecolor='#5C8BC6')

    def choose_plot(label):
        """On button click, switch between lissajous & polar plots.

        label: string of choose_plot button label, Polar or Lissajous.
        """
        if label == 'Lissajous':
            pol_ax.set_visible(False)
            float_ax.set_visible(True)

        if label == 'Polar':
            pol_ax.set_visible(True)
            float_ax.set_visible(False)
        fig.canvas.draw_idle()

    # Connect button click event to callback function
    # to switch between plots
    polarlissa.on_clicked(choose_plot)

    # Labelsize & color for polarlissa buttons
    for label in polarlissa.labels:
        label.set_fontsize(8)
        label.set_color('#F9A438')

    # Dynamically resize radio button height with figure size
    # & setting color and width of button edges
    rpos = rax.get_position().get_points()
    fig_height = fig.get_figheight()
    fig_width = fig.get_figwidth()
    rscale = (rpos[:,1].ptp()/rpos[:,0].ptp()) * (fig_height/fig_width)
    for circ in polarlissa.circles:
        circ.height /= rscale
        circ.set_edgecolor('#F9A438')
        circ.set_lw(0.5)

    # Hide button axes
    rax.set_visible(False)

    # Store text to be resized
    if resize_ls is not None:
        for label in theta_labels:
            resize_ls.append(label)

        resize_ls.extend([title_vec, float_title, l_pos, l_neg, r_pos, r_neg])

    # Individual figure or as part of larger figure
    if sub:
        return fig, resize_ls, polarlissa, choose_plot
    else:
        return plt.show()