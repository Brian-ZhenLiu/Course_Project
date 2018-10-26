import math 
import numpy as np
import scipy.signal as si
from numpy import *
from PIL import Image
from scipy import signal
from PIL import ImageDraw

def gKernel(sigma, radius):
    s =sigma ** 2
    g = np.zeros( (2 * radius + 1, 2 * radius + 1 ) )
    for y in range(-radius, radius):
        for x in range(-radius, radius):
            g[x, y] = 1 / ( 2 * math.pi * s ) * exp( -(x ** 2 + y ** 2) / (2 * s) )
    return g / sum(g)
   
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

def LucaseKanade(img1, img2, g):
    imgSmooth1 = signal.convolve(img1, g, mode='same')
    imgSmooth2 = signal.convolve(img2, g, mode='same')
    a = np.array(([-1, 1], [-1, 1]))
    b = np.array(([-1, -1], [1, 1]))
    Ix = si.convolve2d(imgSmooth1, a, mode='same') + si.convolve2d(imgSmooth2, a, mode='same')
    Iy = si.convolve2d(imgSmooth1, b, mode='same') + si.convolve2d(imgSmooth2, b, mode='same')
    #Ix, Iy = np.gradient(imgSmooth)
    It = si.convolve2d(img1, np.ones((2,2))) + si.convolve2d(img2, -1 * np.ones((2,2)))
    It = It[0:It.shape[0]-1, 0:It.shape[1]-1]
    return Ix, Iy, It 


def draw(V0, V1, img):
    img = img.convert('RGB')
    draw = ImageDraw.Draw(img)
    for i in range(0, V0.shape[0],5):
        for j in range(0, V1.shape[1],5):
            if (V0[i][j]**2 +  V1[i][j]**2)**0.5 > 3:
                draw.line( (i, j) + (i+V0[i][j], j+V1[i][j]), fill=255)
    img.show()
 
def main(file1, file2, g):
    img1 = Image.open(file1).convert('L')
    img2 = Image.open(file2).convert('L')
    imgArr1 = np.array(img1).T
    imgArr2 = np.array(img2).T
    fx, fy, ft = LucaseKanade(imgArr1, imgArr2, g)
    #input window size here
    V0, V1 = window(fx, fy, ft, 11)
    draw(V0, V1, img2)
    
# adjust gaussian kernel
g = gKernel(1.5, 1)
main("basketball1.png", "basketball2.png", g)
main("grove1.png", "grove2.png", g)
