import numpy as np
from PIL import Image
import pylab as plt

# calculate histogram
def histogram(grayImg):
    imgArr = np.array(grayImg)
    his = np.zeros( (256) )
    for i in range(256):
        temp = where(imgArr == i)
        his[i] = temp[0].shape[0]
    return his

# implement histogram Equalization algorithm
def histogramEqualization(his,image):
    arr = np.array(image)
    equalImg = np.zeros((arr.shape[0],arr.shape[1]))
    for i in range(arr.shape[0]):
        for j in range(arr.shape[1]):
            numSum = 0
            for k in range(arr[i,j]):
                numSum = numSum + his[k]
            equalImg[i,j] = round(255 * numSum / (arr.shape[0] * arr.shape[1]))
    print(equalImg)
    newImage = Image.fromarray(equalImg)
    return newImage
    
def main(file):
    Img = Image.open(file).convert('L')
    his = histogram(Img)
    equalImg = histogramEqualization(his, Img)
    equalImg.show()
    afterHis = histogram(equalImg)
    plt.plot(his)
    plt.plot(afterHis)

main('02.jpg')