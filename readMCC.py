#interface to MCC USB-1208FS 
#using Andrew Straw's Universal LIbrary wrapper
#following the example in ulai01.py, ulai14.py

import UniversalLibrary as UL
import numpy
import matplotlib.pyplot as plt
import scipi.io.wavfile as siw
#%%
#setup the board
boardNum = 0
gain = UL.BIP5VOLTS
lowChan = 0
highChan=1
options=UL.CONVERTDATA

#set up acquisition duration
#sampleRate=20000#Hz
#sampleDur=30#seconds
#sampleNum=sampleRate*sampleDur
sampleNum=2**19 #makes the FFT go better
sampleDur=30.0 #s
sampleRate=sampleNum/sampleDur #can this be a float?
#setup array to hold data
analogData=numpy.zeros((sampleNum,),dtype=numpy.int16)


#while 1:
    #read a value
#    dataValue = UL.cbAIn(boardNum, chan, gain)
    #convert analog "count" value to volts
#    engUnits = UL.cbToEngUnits(boardNum, gain, dataValue)

#collect data in a loop until user asks to stop
cont=1
nextSample=input('enter next sample name:\n')
nextSample.replace(' ','_')
while cont==1:
    #actually collect the data
    print('starting data collection') 
    actualRate = UL.cbAInScan(boardNum, lowChan, highChan, sampleNum,
                              sampleRate, gain, analogData,options)   
    print('data collection complete')
    
    #take FFT
    #following matlab code to try and get scaling right--need to check
    complexFreqData=numpy.fft.fft(analogData)/sampleNum
    freqData=complexFreqData[:sampleNum/2+1]
    frequencies=actualRate/2*numpy.linspace(0,1,sampleNum/2+1)
    
    plt.figure(figsize=(8,6),dpi=50)
    plt.subplot(2,1,1)
    fakeX=numpy.linspace(0,sampleNum,sampleNum)
    plt.plot(fakeX,analogData,'-')
    plt.xlabel('time (s)')
    plt.ylabel('voltage (V)')
    plt.subplot(2,1,2)
    plt.plot(frequencies,2*numpy.abs(freqData),'.')
    plt.xlabel('frequency (Hz)')
    plt.ylabel('amplitude')
    figName=nextSample+'.png'
    plt.savefig(figName)
    
    #save data to a wave file
    wavFile=nextSample+'.wav'
    #might need to scale the data to max of 80?
    #http://stackoverflow.com/questions/18645544/writing-wav-file-in-python-with-wavfile-write-from-scipy
    siw.write(wavFile,actualRate,analogData)

    #get the next sample name
    nextSample=input('enter next sample name (x to quit):\n')
    if nextSample=='x':
        cont=0
    else:
        nextSample.replace(' ','_')
