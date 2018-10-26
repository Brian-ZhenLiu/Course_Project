import math 
import numpy as np
from PIL import Image
# plot binary image by threshold level T
def binaryImg(img, threshold):
    temp = np.array(img)
    high = where(temp >= threshold)
    low = where(temp < threshold)
    temp[high] = 255
    temp[low] = 0
    newImage = Image.fromarray(temp)
    return newImage

#calculate entropy based on probability
def entropy(prob):
    entropies = np.zeros( (256) )
    for i in range(1, 256):
        entropyA = 0
        entropyB = 0
        logEntropyA = 0
        logEntropyB = 0
        entropyA = sum(prob[0 : i])
        entropyB = sum(prob[i : 256])
        logProb = np.zeros( (256) )
        for j in range(0,256):
            if prob[j] != 0:
                logProb[j] = np.log(prob[j])
        if (entropyA == 0) or (entropyB == 0):
            entropies[i] = 0
        else:
            logEntropyA = sum(np.multiply(prob[0 : i], logProb[0 : i]))
            logEntropyB = sum(np.multiply(prob[i : 256], logProb[i : 256]))
            entropies[i] =  math.log(entropyA) + math.log(entropyB) - logEntropyA / entropyA - logEntropyB / entropyB
    print(argmax(entropies))
    return argmax(entropies)

# calculate probability based on histogram
def PDF(his):
    sumOfPix = sum(his)
    prob = np.zeros( (256) )
    for i in range(256):
        prob[i] = his[i] / sumOfPix
    return prob

# calculate histogram
def histogram(grayImg):
    imgArr = np.array(grayImg)
    his = np.zeros( (256) )
    for i in range(256):
        temp = where(imgArr == i)
        his[i] = temp[0].shape[0]
    return his

# main function to implement other functions 
def main(file):
    I = Image.open(file)
    his = histogram(I)
    prob = PDF(his)
    T = entropy(prob)
    binaryImage = binaryImg(I,T)
    binaryImage.show()
    
main('03.jpg')