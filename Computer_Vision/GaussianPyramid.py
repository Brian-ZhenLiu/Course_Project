import math 
import numpy as np
import scipy.signal as si
from numpy import *
from PIL import Image
from scipy import signal
from PIL import ImageDraw

# create gaussian kernel
def gKernel(sigma, radius):
    s =sigma ** 2
    g = np.zeros( (2 * radius + 1, 2 * radius + 1 ) )
    for y in range(-radius, radius):
        for x in range(-radius, radius):
            g[x, y] = 1 / ( 2 * math.pi * s ) * exp( -(x ** 2 + y ** 2) / (2 * s) )
    return g / sum(g)

# use Lucas Kanade method to generate Ix,Iy,It
def LucaseKanade(imgSmooth1, imgSmooth2, g):
    a = np.array(([-1, 1], [-1, 1]))
    b = np.array(([-1, -1], [1, 1]))
    Ix = si.convolve2d(imgSmooth1, a, mode='same') + si.convolve2d(imgSmooth2, a, mode='same')
    Iy = si.convolve2d(imgSmooth1, b, mode='same') + si.convolve2d(imgSmooth2, b, mode='same')
    It = si.convolve2d(imgSmooth1, np.ones((2,2))) + si.convolve2d(imgSmooth2, -1 * np.ones((2,2)))
    It = It[0:It.shape[0]-1, 0:It.shape[1]-1]
    return Ix, Iy, It 
 
# create window to calculate V vector   
def window(fx, fy, ft, windowSize):
    winRadius = (int)(windowSize / 2)
    V0 = np.zeros(fx.shape)
    V1 = np.zeros(fx.shape)
    for i in range(winRadius, fx.shape[0] - winRadius):
        for j in range(winRadius, fx.shape[1] - winRadius):
            Ix = fx[i - winRadius:i + winRadius, j - winRadius:j + winRadius].flatten(order='F')
            Iy = fy[i - winRadius:i + winRadius, j - winRadius:j + winRadius].flatten(order='F')
            It = -ft[i - winRadius:i + winRadius, j - winRadius:j + winRadius].flatten(order='F')
            A = np.vstack((Ix, Iy)).T
            V0[i][j], V1[i][j] = np.dot(np.dot(np.linalg.pinv(np.dot(A.T,A)),A.T),It) 
            if math.isnan(V0[i][j]):
                V0[i][j] = 0
            if math.isnan(V1[i][j]):
                V1[i][j] = 0
    return V0,V1


# create gaussian pyramid and return the last level's image
def pyramid(level, lastImg):
    for l in range(1,level + 1):
        imgScale = np.zeros(((int)(lastImg.shape[0]/2),(int)(lastImg.shape[1]/2)))
        imgSmooth = signal.convolve(lastImg, g, mode='same')
        for i in range(imgScale.shape[0]):
            for j in range(imgScale.shape[1]):
                imgScale[i][j] = imgSmooth[2*i][2*j]
        lastImg = imgScale
    return lastImg

#   zoom in V vector 
def zoomIn(level, sArr):
    for l in range(1,level + 1):
        newArr = np.zeros((sArr.shape[0] * 2, sArr.shape[1] * 2))
        for i in range(sArr.shape[0]):
            for j in range(sArr.shape[1]):
                newArr[2*i][2*j] = newArr[2*i+1][2*j] = newArr[2*i+1][2*j] = newArr[2*i+1][2*j] = sArr[i][j] 
        sArr = newArr
    return (sArr)

# draw flow
def draw(V0, V1, img):
    img = img.convert('RGB')
    draw = ImageDraw.Draw(img)
    for i in range(0, V0.shape[0],5):
        for j in range(0, V1.shape[1],5):
            #if (V0[i][j]**2 +  V1[i][j]**2)**0.5 > 1:
            draw.line( (i, j) + (i+V0[i][j]*4, j+V1[i][j]*4), fill=255)
    img.show()

def main(file1, file2, g,level):
    img1 = Image.open(file1).convert('L')
    img2 = Image.open(file2).convert('L')
    imgArr1 = np.array(img1).T
    imgArr2 = np.array(img2).T
    # do gaussian smooth
    imgSmooth1 = signal.convolve(img1, g, mode='same')
    imgSmooth2 = signal.convolve(img2, g, mode='same')
    # do lucas kanade generate Ix,Iy,It
    fx, fy, ft = LucaseKanade(imgArr1, imgArr2, g)
    V0, V1 = window(fx, fy, ft, 21)
    #draw flow
    draw(V0, V1, img2)
    #generate pyramid and get last level image
    pyramidArr1 = pyramid(level,imgArr1)
    pyramidArr2 = pyramid(level,imgArr2)
    #generate Ix,Iy,It of last image of pyramid
    fx, fy, ft = LucaseKanade(pyramidArr1, pyramidArr2, g)
    V0, V1 = window(fx, fy, ft, 9)
    #calculate origin size V vector
    V0 = zoomIn(level,V0)
    V1 = zoomIn(level,V1)
    draw(V0, V1, img2)

g = gKernel(1.5, 1)
main("basketball1.png", "basketball2.png", g, 1)
main("grove1.png", "grove2.png", g)
