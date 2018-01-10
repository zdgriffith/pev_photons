#!/usr/bin/env python

########################################################################
# Supporting functions and variables
########################################################################

# Directory where files are kept that are only accessed,
# not written to.
resource_dir = '/data/user/zgriffith/pev_photons/resources/'

# The matplotlib plotting stylesheet.
plot_style = resource_dir+'gamma_rays_5yr.mplstyle'

# Directory to store data files that are created from the package scripts.
prefix = '/data/user/zgriffith/pev_photons/'

# Directory to store plots
fig_dir = '/home/zgriffith/public_html/pev_photons/'

# Custom color map in the style of
# the all-sky neutrino point source analysis.
from matplotlib.colors import LinearSegmentedColormap

ps_map = {'blue' : ((0.0, 0.0, 1.0),
                    (0.17, 1.0, 1.0),
                    (0.4, 1.0, 1.0),
                    (0.6, 1.0, 1.0),
                    (0.7, 0.2, 0.2),
                    (1.0, 0.0, 0.0)),
          'green': ((0.0, 0.0, 1.0),
                    (0.17, 1.0, 1.0),
                    (0.5, 0.0416, 0.0416),
                    (0.6, 0.0, 0.0),
                    (0.8, 0.5, 0.5),
                    (1.0, 1.0, 1.0)),
          'red':   ((0.0, 0.0, 1.0),
                   (0.17, 1.0, 1.0),
                   (0.5, 0.0416, 0.0416),
                   (0.6, 0.0416, 0.0416),
                   (0.7, 1.0, 1.0),
                    (1.0, 1.0, 1.0))}

ps_map = LinearSegmentedColormap('ps_map', ps_map, 256)

def plot_setter(ax, legend = None, bg_color = 'white', text_color='#262626'):
    """ Make the lines thicker in the legend, standardize text colors """

    ax.set_axis_bgcolor(bg_color)
    for tick in ax.get_xticklines():
        tick.set_color(text_color)
    for tick in ax.get_yticklines():
        tick.set_color(text_color)
    if legend: 
        for text in legend.get_texts():
            text.set_color(text_color)
        for legobj in legend.legendHandles:
            legobj.set_linewidth(3.0)
