#interface to MCC USB-1208FS 
#using Andrew Straw's Universal LIbrary wrapper
#following the example in ulai01.py

import UniversalLibrary as UL
import numpy
import matplotlib.pyplot as plt

#%%
BoardNum = 0
Gain = UL.BIP5VOLTS
Chan = 0

while 1:
    DataValue = UL.cbAIn(BoardNum, Chan, Gain)
    EngUnits = UL.cbToEngUnits(BoardNum, Gain, DataValue)

    print DataValue, EngUnits
