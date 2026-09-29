

import statistics


def Median(mylist, empty_index):
    if( mylist!=[] ):
        return statistics.median(mylist)
    elif( mylist==[] ):
        return empty_index
    