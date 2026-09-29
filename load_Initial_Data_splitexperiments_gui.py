

from asyncio.windows_events import NULL


import os,sys,inspect

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir)


from globalVars import guiflag
from gui_splitexperiments import gui_splitexperiments


def Load_Initial_splitexperiments_gui():
    if( guiflag ):
        subs = NULL
        while( subs==NULL ):
            subs, texts = gui_splitexperiments()

    else:
        # texts = [ 'visit', 'zoo', 'visitloud', 'psaras', 'morning', 'island', 'efeyreseis', 'zebra', 'armyjet', 'enemypie', 'gasmask', 'jockey', 'midfred', 'midfredloud', 'sunny', 'sunnyloud' ]
        # texts = ['visit', 'visitloud', 'zoo', 'psaras', 'efeyreseis', 'sunny', 'midfred', 'midfredloud', 'armyjet', 'gasmask']
        # texts = ['zoo', 'visit']
        # texts = ['visit', 'zoo', 'zebra', 'visitloud']
        # texts = ['visualorthogrecognpart1']
        # texts = ['adk1k2part1', 'adk1k2part2', 'adk3k4part1', 'adk3k4part2', 'adk5k6part1', 'adk5k6part2']
        # texts = ['adk1k2part1']
        texts = ['efivk1k2', 'efivk3k4', 'efivk5k6']
        
        
        # texts = ['visualorthogrecognpart1', 'visualorthogrecognpart2']
        # texts = ['zoo', 'visit', 'efeyreseis', 'olympia', 'morning', 'zebra', 'visitloud']
        
        # subs = [1455, 1456, 1459, 1460, 1461]
        subs = [ person  for person  in range(1941, 1957) ]
        # subs = [x for x in range(13680, 13700)]
        # subs = [13003, 13017, 13044, 13054, 13058, 13066, 13070, 13086, 13105, 13108, 13158, 13161, 13166, 13167, 13172, 13178, 13198, 13203, 13209, 13222, 13234]
        # subs = [14315]
        # subs = [1419]
        # subs = [1488, 1490, 1424, 1431, 1441, 1461, 1482, 1531, 1532, 1580, 1632]   #ofthalmos list, me exophoria oi 5 teleftaioi
        # subs = [subno for subno in range(14420, 14440)]
        # subs = [sno for sno in range(1868, 1869)] #1868, 561 done

        
        bypass = 1
        hardcases = 0
        onlylefteye = 0
        onlyrighteye = 0
        firstchoices = [bypass, hardcases, onlylefteye, onlyrighteye]
    
    return subs, texts