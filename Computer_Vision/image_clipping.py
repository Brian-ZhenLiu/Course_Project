import math 
import numpy as np
from PIL import Image

# implement Clipping algorithm
def clipping(image, a, b, beta):
    arr = np.array(image)
    newArr = np.zeros((arr.shape[0],arr.shape[1]))
    for i in range(arr.shape[0]):
        for j in range(arr.shape[1]):
            if arr[i,j] >= a and arr[i,j] < b:
                newArr[i,j] = beta * (arr[i,j] - a)
            elif arr[i,j] >= b:
                newArr[i,j] = beta * (b - a)
    newImage = Image.fromarray(newArr)
    return newImage

# implement  range compression algorithm 
def rangeCompression(image,c):
    arr = np.array(image)
    newArr = np.zeros((arr.shape[0],arr.shape[1]))
    for i in range(arr.shape[0]):
        for j in range(arr.shape[1]):
            newArr[i,j] = c * math.log10(arr[i,j] + 1)
    newImage = Image.fromarray(newArr)
    return newImage


def main(file):
    Img = Image.open(file).convert('L')
    imgClipping = clipping(Img, 50, 150, 2)
    imgClipping.show()
    rangeCompression(Img, 1).show()
    rangeCompression(Img, 10).show()
    rangeCompression(Img, 100).show()
    rangeCompression(Img, 1000).show()
    
main('01.jpg')
                