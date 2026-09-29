

import matplotlib.pyplot as plt


def find_y_fromhist(tempy):
    # Friday Add-on: Calculate with histograme the space with most occurances and find the index(y) of it 
    num_bins = 100
    nonzerosy = [x for x in tempy if x!=-1]  # to nonzeros y exei ola ta gazes kai ta valid kai ta nonvalid. Gia na ipologisw omws th median ta -1 mou einaio axrista kai ta petaw.
    n, bins, patches = plt.hist(nonzerosy, num_bins, 
                density = 1, 
                color ='green',
                alpha = 0.7)
    plt.close()
    bins = bins.tolist()
    n = n.tolist()
    N =[]
    for k in range(len(n)):
        N.append( round(n[k], 5) )

    maxn = max(N)
    index = N.index(maxn)

    # print("maxn = ", maxn)
    # print("index = ", index)
    # print("bins[index] = ", bins[index] )
   
    # plt.show()

    avg = (bins[index] + bins[index+1])/2
    return avg