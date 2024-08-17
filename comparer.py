import crepe
import math
import numpy as np
import statistics
from scipy.io import wavfile
import tensorflow as tf



def combinedata(n,list):
    newlist = []
    temp = 0
    for x in range (0,len(list)):
        temp += list[x]
        if x%n == 0:
            temp = temp/n
            newlist.append(temp)
            temp = 0
    return newlist

def compareaudios(file1, file2):
    sr1, audio1 = wavfile.read(file1)
    sr2, audio2 = wavfile.read(file2)

    time1, frequency1, confidence1, activation1 = crepe.predict(audio1, sr1, model_capacity='tiny', viterbi=True)
    time2, frequency2, confidence2, activation2 = crepe.predict(audio2, sr2, model_capacity='tiny', viterbi=True)
    
    # print(pitchattime(time1,frequency1))
    frequency1=combinedata(10,frequency1)
    frequency2=combinedata(10,frequency2)

    diff = []

    for x in range (0,min(len(frequency1),len(frequency2))):
        # frequency1[x]=removeoctave(frequency1[x],frequency2[x])
        if abs(frequency1[x]-frequency2[x])<=2:
            temp = 0
        elif frequency2[x]>frequency1[x]:
            temp = frequency1[x]-frequency2[x]+2
        else:
            temp = frequency1[x]-frequency2[x]-2

        # diff.append(temp*confidence2[x])
        diff.append(temp)

    netdiff = statistics.mean((abs(x) for x in diff))
    print(netdiff)
    return(netdiff)

def removeoctave(fr1, fr2):
    if fr1>fr2:
        l = math.floor(math.log(fr1/fr2,2))
        return(fr1/pow(2,l))
    else:
        l = math.floor(math.log(fr2/fr1,2))
        return (fr1*pow(2,l))

# def pitchattime(time, frequency):
#     pitches = []
#     prevf = frequency[0]
#     prevt = time[0]
#     temp = 0
#     cnt = 0
#     for x in range(0,len(frequency)):
#         temp += frequency[x]
#         cnt += 1
#         if time[x]-prevt>0.25:
#             temp/=cnt
#             pitches.append([time[x],temp])
#             prevf=temp
#             temp = 0
#             cnt = 0
#             prevt=time[x]
#     return pitches

#calculate a percentage score from 0 - 100
def scaleToScore(netDiff):
    return round(((1 - ((netDiff) / 200)) * 100), 2)


