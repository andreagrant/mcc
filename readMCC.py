#interface to MCC USB-1208FS 
#using Andrew Straw's Universal LIbrary wrapper
#following the example in ulai01.py, ulai14.py
# https://scipy.github.io/old-wiki/pages/Cookbook/Data_Acquisition_with_PyUL.html
import UniversalLibrary as UL
import numpy
import matplotlib.pyplot as plt
import scipy.io.wavfile as siw

#%%
#setup the board
boardNum = 0
#gain = UL.BIP5VOLTS
gain = UL.BIP20VOLTS
#gain=UNIPT25VOLTS
lowChan = 0
highChan=0
Options=UL.CONVERTDATA

#set up acquisition duration
#sampleRate=20000#Hz
#sampleDur=30#seconds
#sampleNum=sampleRate*sampleDur
sampleNum=2**18 #makes the FFT go better
sampleDur=10.0 #s
sampleRate=int(numpy.floor(sampleNum/sampleDur)) #can this be a float? nope
print(sampleRate)
#setup array to hold data
analogData=numpy.zeros((sampleNum,),dtype=numpy.int16)


#while 1:
    #read a value
#    dataValue = UL.cbAIn(boardNum, chan, gain)
    #convert analog "count" value to volts
#    engUnits = UL.cbToEngUnits(boardNum, gain, dataValue)

#collect data in a loop until user asks to stop
nextSample=''
#nextSample=input('enter next sample name:\n')
nextSample=raw_input('enter next sample name:\n')
if nextSample=='x':
    cont=0
else:
    cont=1
    nextSample.replace(' ','_')
#%%
while cont==1:
    analogData=numpy.zeros((sampleNum,),dtype=numpy.int16)
    #actually collect the data
    print('starting data collection') 
    actualRate = UL.cbAInScan(boardNum, lowChan, highChan, sampleNum,
                              sampleRate, gain, analogData,Options)   
    print('data collection complete')
    voltData = numpy.asarray([ UL.cbToEngUnits(boardNum, gain, int(y)) for y in analogData])

    #take FFT
    #following matlab code to try and get scaling right--need to check
    complexFreqData=numpy.fft.fft(voltData)/sampleNum
    freqData=complexFreqData[:sampleNum/2+1]
    frequencies=actualRate*numpy.linspace(0,1,sampleNum/2+1)
    db=10*numpy.log10(2*numpy.abs(freqData))
    
    plt.figure(figsize=(16,6),dpi=50)
    plt.subplot(2,1,1)
    fakeX=numpy.linspace(0,sampleNum,sampleNum)/actualRate
    downsample=100
    plt.plot(fakeX[0::downsample],voltData[0::downsample],'-',linewidth=0.1)
    plt.xlabel('time (s)')
    plt.ylabel('voltage (V)')
    plt.grid()
    
    plt.subplot(2,1,2)
    plt.plot(frequencies,db,'x')
    plt.xlabel('frequency (Hz)')
    plt.ylabel('power (dB)')
    plt.xlim(-10,20000)
    plt.minorticks_on()
    plt.grid(which='both')
    figName=nextSample+'.png'
    plt.savefig(figName)
    plt.close()
    #save data to a wave file
    wavFile=nextSample+'.wav'
    #might need to scale the data to max of 80?
    #http://stackoverflow.com/questions/18645544/writing-wav-file-in-python-with-wavfile-write-from-scipy
    siw.write(wavFile,actualRate,voltData)

    #get the next sample name
    nextSample=raw_input('enter next sample name (x to quit):\n')
    if nextSample=='x':
        cont=0
    else:
        nextSample.replace(' ','_')
