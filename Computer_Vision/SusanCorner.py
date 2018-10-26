import numpy as np
from PIL import Image
from PIL import ImageDraw
import math

# 37 pixels circular mask
mask = np.array([[0,0,1,1,1,0,0],
                [0,1,1,1,1,1,0],
                [1,1,1,1,1,1,1],
                [1,1,1,1,1,1,1],
                [1,1,1,1,1,1,1],
                [0,1,1,1,1,1,0],
                [0,0,1,1,1,0,0]])
    
def susan(image, mask, t):
    arr = np.array(image)
    height, width = arr.shape
    R = np.zeros((height,width))
    nAreaUSAN = np.zeros((height,width))
    for i in range(3, height - 3):
        for j in range(3, width - 3):
            underMask = arr[i - 3 : i + 4 , j - 3 : j + 4]
            cUSAN = exp(- ( (underMask - arr[i, j]) / t) ** 6)
            countUSAN = np.multiply(cUSAN, mask)
            nAreaUSAN[i,j] = sum(countUSAN) - 1          
    gThreshold = nAreaUSAN[(int)(argmax(nAreaUSAN) / width), argmax(nAreaUSAN) % height] * 0.5
    print(gThreshold)
    for i in range(3, height - 3):
        for j in range(3, width - 3):
            if nAreaUSAN[i,j] < gThreshold:
                R[i,j] = gThreshold - nAreaUSAN[i,j]
    return R
# non-max suppression operation
def nonMaxSuppression(R):
    newR = np.zeros(R.shape)
    for i in range(1,R.shape[0]):
        for j in range(1,R.shape[1]):
            neighbor = R[i - 1 : i + 2, j - 1 : j + 2]
            if argmax(neighbor) == 4:
                newR[i,j] = R[i,j]
    return newR

#  create a function to draw the corners which is detected by former algorithms        
def drawCircleOnImg(Img, R):
    Img = Img.convert('RGB')
    draw = ImageDraw.Draw(Img)
    count = 0
    for i in range(R.shape[0]):
        for j in range(R.shape[1]):
            if R[i, j] > 0:
                draw.ellipse( (j - 1, i - 1, j + 1, i + 1), outline ='orange')
                count = count + 1
    print( "total circle drawing : " + str(count) )
    Img.show() 

def mFilter(arr):
    width, height = arr.shape
    newArr = np.zeros(arr.shape)
    for x in range(1, width - 1):
        for y in range(1, height - 1):
            partArr = arr[x - 1: x + 2, y - 1: y + 2]
            temp = np.zeros(9)
            for i in range(3):
                for j in range(3):
                    temp[i*3+j] = partArr[i, j]
            temp.sort()
            newArr[x, y] = temp[4]
    return newArr

def convolve(arr, mask):
    maskSize = mask.shape[0]
    width, height = arr.shape
    newArr = np.zeros(arr.shape)
    for x in range((int)(maskSize/2), width - (int)(maskSize/2)):
        for y in range((int)(maskSize/2), height - (int)(maskSize/2)):
            temp = arr[x - (int)(maskSize/2): x + (int)(maskSize/2) + 1, 
                                y - (int)(maskSize/2): y + (int)(maskSize/2) + 1]
            newArr[x, y] = sum(np.multiply(temp, mask))
            newImage = Image.fromarray(newArr)
    return newImage

def gaussian(sigma, size):
    (X, Y)= ( (size - 1) / 2, (size - 1) / 2)
    s2 = 2.0 * (sigma**2)
    gauss = np.zeros( (size, size) )
    for y in range(size):
        for x in range(size):
            x2 = (x - X)**2
            y2 = (y - Y)**2
            gauss[x, y] = 1 / ( 2 * math.pi * sigma**2 ) * exp( -(x2 + y2) / s2 )
    return gauss / sum(gauss)
    
# main function to implement other functions 
def main(file):
    sigma = 0.2
    size = 11
    Img = Image.open(file).convert('L')
    arr = np.array(Img)
    R = susan(Img, mask, 20)
    nmsR = nonMaxSuppression(R)
    #drawCircleOnImg(Img, nmsR)
    medianImgArr = mFilter(arr)
    medianImg = Image.fromarray(medianImgArr)
    medianImg.show()
    G = gaussian(sigma, size)
    blurImg = convolve(medianImgArr, G)
    smoothR = susan(blurImg, mask, 10)
    nmsR =  nonMaxSuppression(R)
    nmsSmoothR = nonMaxSuppression(smoothR)
    drawCircleOnImg(medianImg, nmsSmoothR)

main('susan_input2.png')
           
