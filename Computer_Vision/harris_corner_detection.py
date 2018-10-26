import math 
import numpy as np
from numpy import *
from PIL import Image
from PIL import ImageDraw
from scipy import signal
import time

class harrisCorner:
     # initialize radius and siama  
    def __init__(self, radius, sigma):  
        self.radius=radius  
        self.sigma=sigma 
        
    # Gaussian function calculate
    def gaussianFunc(self,x):
        gauss1 = 1/(pow(2*math.pi*self.sigma*self.sigma,0.5))  
        gauss2 = math.exp(-(x*x)/(2*self.sigma*self.sigma))
        return gauss1 *gauss2
    
    # create one-dimentional Gaussian mask
    def gaussmask(self):
        maskSize = self.radius * 2 + 1
        mask = np.zeros((maskSize, 1))
        for i in range(maskSize):
            mask[i] = self.gaussianFunc(i-self.radius)       
        return mask
    
    # smooth operation using gaussian mask
    def smooth(self,arr):
        newData = np.zeros((arr.shape[0],arr.shape[1]))
        gaussianMask = self.gaussmask() 
        gaussianMask = gaussianMask.T / gaussianMask.sum()
        for i in range(self.radius, arr.shape[0]-self.radius):  
            for j in range(self.radius, arr.shape[1]-self.radius):  
                temp1 = arr[i, j-self.radius:j+self.radius+1]  
                temp2 = np.multiply(temp1, gaussianMask)  
                newData[i, j] = temp2.sum()  
        return newData
    # calculate derivative of Image in x and y directions 
    # calculate second-order derivative and cross direction derivative
    def derivative(self,image):
        arr = np.array(image)
        IxSquare = np.zeros((arr.shape[0], arr.shape[1]))
        IySquare = np.zeros((arr.shape[0], arr.shape[1]))
        IxIy = np.zeros((arr.shape[0], arr.shape[1]))
        derivativeMask = np.array([-1,0,1])
        for i in range(1, arr.shape[0]-1):  
            for j in range(1, arr.shape[1]-1):  
                xtemp1 = arr[i, j - 1 : j + 2]  
                xtemp2 = np.multiply(xtemp1, derivativeMask) 
                ytemp1 = arr[i - 1 : i + 2, j]
                ytemp2 = np.multiply(ytemp1, derivativeMask.T)
                IxSquare[i, j] = xtemp2.sum() ** 2
                IySquare[i, j] = ytemp2.sum() ** 2 
                IxIy[i, j] = xtemp2.sum() * ytemp2.sum()
        return IxSquare, IySquare, IxIy
    
    # calculate the cornerness measure with Det and trace
    def cornerness(self,image,alpha):
        IxSquare, IySquare, IxIy = self.derivative(image)
        matrixA = self.smooth(IxSquare)
        matrixB = self.smooth(IySquare)
        matrixC = self.smooth(IxIy)
        det = np.zeros((matrixA.shape[0],matrixA.shape[1]))
        trace = np.zeros((matrixA.shape[0],matrixA.shape[1]))
        cornerness = np.zeros((matrixA.shape[0],matrixA.shape[1]))
        start = time.time()
        for i in range(matrixA.shape[0]):
            for j in range(matrixA.shape[1]):
                det[i,j] = matrixA[i,j] * matrixB[i,j] - matrixC[i,j] ** 2
                trace[i,j] = matrixA[i,j] + matrixB[i,j]
                cornerness[i,j] =  det[i,j] - alpha * trace[i,j] ** 2
        end = time.time()
        print("Operating time of system: Det(H2) - alpha * Tr(H2) = " + str(end - start) )
        return cornerness
    
    # calculate cornerness measure  with eigen value
    def cornernessEigen(self,image,alpha):
        arr = np.array(image)
        lambda1 = np.zeros((arr.shape[0],arr.shape[1]))
        lambda2 = np.zeros((arr.shape[0],arr.shape[1]))
        IxSquare, IySquare, IxIy = self.derivative(image)
        matrixA = self.smooth(IxSquare)
        matrixB = self.smooth(IySquare)
        matrixC = self.smooth(IxIy)
        cornernessEig = np.zeros((arr.shape[0],arr.shape[1]))
        start = time.time()
        for i in range(arr.shape[0]):
            for j in range(arr.shape[1]):
                temp = np.array( [ [ matrixA[i, j] , matrixC[i, j] ], [ matrixC[i, j], matrixB[i, j] ] ] )
                eigValue , eigVector = np.linalg.eig(temp)
                lambda1[i][j] = eigValue[0]
                lambda2[i][j] = eigValue[1]
                cornernessEig[i,j] = lambda1[i,j] * lambda2[i,j] - alpha * (lambda1[i,j] + lambda2[i,j])
        end = time.time()     
        print("Operating time of system: L1*L2 - alpha * (L1+L2) = " + str(end - start) )
        return cornernessEig

    
#  create a function to draw the corners which is detected by former algorithms     
def drawCircleOnImg(Img, cornerness):
    Img = Img.convert('RGB')
    draw = ImageDraw.Draw(Img)
    count = 0
    for i in range(cornerness.shape[0]):
        for j in range(cornerness.shape[1]):
            if cornerness[i, j] > 7 * 10 ** 7:
                draw.rectangle( (j - 2, i - 2, j + 2, i + 2), outline ='orange')
                count = count + 1
    print( "total circle drawing : " + str(count) )
    Img.show()  
    
 # main function to implement other functions    
def main(file):
    r = 1 #radius  
    s = 1.5 #sigma  
    img = Image.open(file).convert('L')
    hc = harrisCorner(r,s)
    imgCorner = hc.cornerness(img,0.04)
    imgCornerEig = hc.cornernessEigen(img, 0.04) 
    temp = where(imgCorner > 0)
    drawCircleOnImg(img,imgCorner)
    drawCircleOnImg(img,imgCornerEig)
    
main('input1.png')

        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        