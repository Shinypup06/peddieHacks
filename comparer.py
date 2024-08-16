import crepe
import math
from scipy.io import wavfile

def combinedata(n,list):
    newlist = []
    temp = 0
    for x in range (0,len(list)):
        temp = temp+list[x]
        if x%n == 0:
            temp = temp/n
            newlist.append(temp)
            temp = 0
    return newlist

def compareaudios(file1, file2):
    sr1, audio1 = wavfile.read('ViolinA.wav')
    sr2, audio2 = wavfile.read('A.wav')
    time1, frequency1, confidence1, activation1 = crepe.predict(audio1, sr1, viterbi=True)
    time2, frequency2, confidence2, activation2 = crepe.predict(audio2, sr2, viterbi=True)

    frequency1=combinedata(20,frequency1)
    frequency1=combinedata(20,frequency2)

    diff = []

    for x in range (0,min(len(frequency1),len(frequency2))):
        frequency1[x]=removeoctave(frequency1[x],frequency2[x])
        diff.append(frequency1[x]-frequency2[x])

    print(netdiff(diff))
    return(diff)

def removeoctave(fr1, fr2):
    if fr1>fr2:
        l = math.floor(math.log(fr1/fr2,2))
        return(fr1/pow(2,l))
    else:
        l = math.floor(math.log(fr2/fr1,2))
        return (fr1*pow(2,l))

def netdiff(diff):
    temp = 0
    for x in diff:
        temp = temp + abs(x)
    return temp/len(diff)

compareaudios(1,1)
