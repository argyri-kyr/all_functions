
from matplotlib.colors import LinearSegmentedColormap
from mpl_toolkits.axes_grid1 import make_axes_locatable
import matplotlib as mpl

def colorbar(f, ax):

    vmax = 4.0
    cmap = LinearSegmentedColormap.from_list('mycmap', [(0 / vmax, 'blue'),
                                                        (1 / vmax, 'cyan'),
                                                        (2 / vmax, 'lime'),
                                                        (3 / vmax, 'yellow'),
                                                        (4 / vmax, 'red')
                                                        ]

                                                        
                                            )

    # norm = mpl.colors.Normalize(vmin=5, vmax=9)

    divider = make_axes_locatable(ax)
    cax = divider.append_axes("right", size="8%", pad=1.4)
    
    cbar = f.colorbar(mpl.cm.ScalarMappable(cmap=cmap),cax=cax)

    cbar.ax.set_yticklabels(['No', 'Low', 'Avg', 'High', 'Higher', 'Highest'])  # vertically oriented colorbar


    