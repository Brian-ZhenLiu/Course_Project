import math 
from numpy import *
import numpy as np
from PIL import Image

class GaussianBlur:
        #initialize radius and siama  
    def __init__(self, radius, sigma):  
        self.radius=radius  
        self.sigma=sigma   
    #Gaussian function calculate
    def gaussianFunc(self,x):
        gauss1 = 1/(pow(2*math.pi*self.sigma*self.sigma,0.5))  
        gauss2 = math.exp(-(x*x)/(2*self.sigma*self.sigma))
        return gauss1 *gauss2
    
    def gaussianDFunc(self,x):
        gauss1 = -x/(pow(2*math.pi*self.sigma**6,0.5))  
        gauss2 = math.exp(-(x*x)/(2*self.sigma*self.sigma))
        return gauss1 *gauss2
    #create one-dimentional Gaussian mask
    def gaussmask(self):
        maskSize = self.radius * 2 + 1
        mask = np.zeros((maskSize, 1))
        for i in range(maskSize):
            mask[i] = self.gaussianFunc(i-self.radius)       
        return mask
    
    def gaussDmask(self):
        maskSize = self.radius * 2 + 1
        mask = np.zeros((maskSize,1))
        for i in range(maskSize):
            mask[i] = self.gaussianDFunc(i-self.radius)       
        return mask
    #convolve image with Gaussian mask
    def smooth(self,image):
        arr=np.array(image)  
        newData=np.zeros((arr.shape[0], arr.shape[1]))
        gaussianMask = self.gaussmask() 
        gaussianMask = gaussianMask.T / gaussianMask.sum()
        print(gaussianMask)
        for i in range(self.radius, arr.shape[0]-self.radius):  
            for j in range(self.radius, arr.shape[1]-self.radius):  
                temp1 = arr[i, j-self.radius:j+self.radius+1]  
                temp2 = np.multiply(temp1, gaussianMask)  
                newData[i, j] = temp2.sum()  
        newImage = Image.fromarray(newData)            
        return newImage   
    
    def Dsmooth(self,image):
        arr=np.array(image)  
        newData=np.zeros((arr.shape[0], arr.shape[1]))
        gaussianDmask = self.gaussDmask() 
        gaussianDmask = gaussianDmask.T / gaussianDmask[0] 
        for i in range(self.radius, arr.shape[0]-self.radius):  
            for j in range(self.radius, arr.shape[1]-self.radius):  
                temp1 = arr[i, j-self.radius:j+self.radius+1]  
                temp2 = np.multiply(temp1, gaussianDmask)  
                newData[i, j] = temp2.sum()  
        newImage = Image.fromarray(newData)            
        return newImage 
    
    def magnitude(self,image1,image2):
        arrX = np.array(image1)
        arrY = np.array(image2)
        magPixel = np.zeros((arrX.shape[0],arrX.shape[1]))
        for i in range(arrX.shape[0]):
            for j in range(arrX.shape[1]):
                magPixel[i,j] = (arrX[i,j]**2 + arrY[i,j]**2)**(1/2)
        newImage = Image.fromarray(magPixel)
        self.theta = np.arctan2(arrY,arrX)
        return newImage
    
    def nonMaxSuppression(self,image):
        newTheta = np.zeros((self.theta.shape[0],self.theta.shape[1]))
        arr = np.array(image)
        newArr = arr
        for i in range(1,newTheta.shape[0]-1):
            for j in range(1,newTheta.shape[1]-1):
                if self.theta[i,j] > -math.pi / 8 and self.theta[i,j] <= math.pi / 8:
                    newTheta[i,j] = 0
                    if(arr[i,j] < arr[i,j-1] or arr[i,j] < arr[i,j+1] ):
                        newArr[i,j] = 0
                elif self.theta[i,j] > math.pi / 8 and self.theta[i,j] <= 3 * math.pi / 8:
                    newTheta[i,j] = math.pi / 4
                    if(arr[i,j] < arr[i-1,j-1] or arr[i,j] < arr[i+1,j+1] ):
                        newArr[i,j] = 0
                elif self.theta[i,j] >= 3 * math.pi / 8 and self.theta[i,j] <= 5 * math.pi / 8:
                    newTheta[i,j] = math.pi / 2
                    if(arr[i,j] < arr[i-1,j] or arr[i,j] < arr[i+1,j] ):
                        newArr[i,j] = 0
                elif self.theta[i,j] >= 5 * math.pi / 8 and self.theta[i,j] <= 7 * math.pi / 8:
                    newTheta[i,j] = 3 * math.pi / 4
                    if(arr[i,j] < arr[i-1,j+1] or arr[i,j] < arr[i+1,j-1] ):
                        newArr[i,j] = 0
                elif self.theta[i,j] >= 7 * math.pi / 8 and self.theta[i,j] <= -7 * math.pi / 8:
                    newTheta[i,j] = 0
                    if(arr[i,j] < arr[i,j-1] or arr[i,j] < arr[i,j+1] ):
                        newArr[i,j] = 0
                elif self.theta[i,j] >= -7 * math.pi / 8 and self.theta[i,j] <= -5 * math.pi / 8:
                    newTheta[i,j] = math.pi / 4
                    if(arr[i,j] < arr[i-1,j-1] or arr[i,j] < arr[i+1,j+1] ):
                        newArr[i,j] = 0
                elif self.theta[i,j] >= -5 * math.pi / 8 and self.theta[i,j] <= -3 * math.pi / 8:
                    newTheta[i,j] = math.pi/2
                    if(arr[i,j] < arr[i-1,j] or arr[i,j] < arr[i+1,j] ):
                        newArr[i,j] = 0
                elif self.theta[i,j] >= -3 * math.pi / 8 and self.theta[i,j] <= -math.pi / 8:
                    newTheta[i,j] = 3 * math.pi / 4
                    if(arr[i,j] < arr[i-1,j+1] or arr[i,j] < arr[i+1,j-1] ):
                        newArr[i,j] = 0
        newImage = Image.fromarray(newArr)      
        return newImage
    
    def isInRange(self,y, x, width, height):
        if x >= width:
            return False
        elif x < 0:
            return False
        elif y >= height:
            return False
        elif y < 0:
            return False
        else:
            return True

    def recursive(self ,y, x, imgArr, tHigh):
        (H, W) = imgArr.shape
        if imgArr[y, x] >= tHigh:
            return 255
        imgArr[y, x] = -1
        if self.isInRange(y - 1, x, W, H):
            if imgArr[y - 1, x] > 0:
                if self.recursive(y - 1, x, imgArr, tHigh) >= tHigh:
                    imgArr[y, x] = 255
                    return 255   
        if self.isInRange(y - 1, x - 1, W, H):
            if imgArr[y - 1, x - 1] > 0:
                if self.recursive(y - 1, x - 1, imgArr, tHigh) >= tHigh:
                    imgArr[y, x] = 255
                    return 255
        if self.isInRange(y, x - 1, W, H):
            if imgArr[y, x - 1] > 0:
                if self.recursive(y, x - 1, imgArr, tHigh) >= tHigh:
                    imgArr[y, x] = 255
                    return 255
        if self.isInRange(y + 1, x, W, H):
            if imgArr[y + 1, x] > 0:
                if self.recursive(y + 1, x, imgArr, tHigh) >= tHigh:
                    imgArr[y, x] = 255
                    return 255
    
        if self.isInRange(y + 1, x + 1, W, H):
            if imgArr[y + 1, x + 1] > 0:
                if self.recursive(y + 1, x + 1, imgArr, tHigh) >= tHigh:
                    imgArr[y, x] = 255
                    return 255

        if self.isInRange(y, x + 1, W, H):
            if imgArr[y, x + 1] > 0:
                if self.recursive(y, x + 1, imgArr, tHigh) >= tHigh:
                    imgArr[y, x] = 255
                    return 255
                
        if self.isInRange(y + 1, x - 1, W, H):
            if imgArr[y + 1, x - 1] > 0:
                if self.recursive(y + 1, x - 1, imgArr, tHigh) >= tHigh:
                    imgArr[y, x] = 255
                    return 255
        
    
        if self.isInRange(y - 1, x + 1, W, H):
            if imgArr[y - 1, x + 1] > 0:
                if self.recursive(y - 1, x + 1, imgArr, tHigh) >= tHigh:
                    imgArr[y, x] = 255
                    return 255
        return 0
    
    def hysteresisThresholding(self,INMS, tHigh, tLow):
        tempINMS = np.array(INMS)
        strong = where(tempINMS >= tHigh)
        tempINMS[strong] = 255
        drop = where(tempINMS <= tLow)
        tempINMS[drop] = 0
        weak = where(tempINMS < tHigh)
    
        for i in range(weak[0].shape[0]):
            y, x = weak[0][i], weak[1][i]
            if tempINMS[y, x] != 0 and tempINMS[y, x] != 255:
                tempINMS[y, x] = self.recursive(y, x, tempINMS, tHigh)
        Iht = Image.fromarray(tempINMS)
        return Iht          

def main(image):                    
    imgPIL = Image.open(image)
    r = 1 #radius  
    s = 2 #sigma  
    GB = GaussianBlur(r, s) 
# image X direction with G
    Ix = GB.smooth(imgPIL)
    Ix.show()
#image Y direction with G
    Iy = GB.smooth(imgPIL.transpose(Image.ROTATE_90))
    Iy = Iy.transpose(Image.ROTATE_270)
    Iy.show()
#image X direction with Gx 
    Ix_ = GB.Dsmooth(Ix)
    Ix_.show()
#image Y direction with Gy
    Iy_ = GB.Dsmooth(Iy.transpose(Image.ROTATE_90))
    Iy_ = Iy_.transpose(Image.ROTATE_270)
    Iy_.show()
    Im = GB.magnitude(Ix_,Iy_)
    Im.show()
    Inms = GB.nonMaxSuppression(Im)
    Inms.show()
    Iht = GB.hysteresisThresholding(Inms, 120, 60)
    Iht.show()
    
main('119082.jpg')
