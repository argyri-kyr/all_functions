

import matplotlib.pyplot as plt

def zoomimage(x, y, width, height):
    max_xw = x[0] + width[0]

    for i in range(len(x)):
        if( x[i] + width[i] > max_xw ):
            max_xw = x[i] + width[i]

    first_x = x[0] - 10
    last_x = max_xw + 10
    plt.xlim(first_x, last_x)
    
    first_y = y[0] - 5
    last_y = y[-1] + height[-1] + 5
    plt.ylim(last_y, first_y)