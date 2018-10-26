import math 
import numpy as np
from numpy import *
from PIL import Image
from PIL import ImageDraw

# calculate derivative of Image in x and y directions
def derivative(arr):
    Ix = np.zeros((arr.shape[0], arr.shape[1]))
    Iy = np.zeros((arr.shape[0], arr.shape[1]))
    derivativeMask = np.array([-1,0,1])
    for i in range(1, arr.shape[0]-1):  
        for j in range(1, arr.shape[1]-1):  
            xtemp1 = arr[i, j - 1 : j + 2]  
            xtemp2 = np.multiply(xtemp1, derivativeMask) 
            ytemp1 = arr[i - 1 : i + 2, j]
            ytemp2 = np.multiply(ytemp1, derivativeMask.T)
            Ix[i, j] = xtemp2.sum() 
            Iy[i, j] = ytemp2.sum()  
    return Ix, Iy

# calculate eigen-value of the given matrix H1 and use it to find corners    
def hessianCornerDetection(image):
    arr = np.array(image)
    lambda1 = np.zeros((arr.shape[0],arr.shape[1]))
    lambda2 = np.zeros((arr.shape[0],arr.shape[1]))
    Ix , Iy = derivative(arr)
    Ixx , Ixy = derivative(Ix)
    Iyx , Iyy = derivative(Iy)
    markArr = np.zeros((arr.shape[0],arr.shape[1]))
    count = 0
    for i in range(arr.shape[0]):
        for j in range(arr.shape[1]):
            temp = np.array( [ [ Ixx[i, j] , Iyx[i, j] ], [ Ixy[i, j], Iyy[i, j] ] ] )
            eigValue , eigVector = np.linalg.eig(temp)
            lambda1[i][j] = eigValue[0]
            lambda2[i][j] = eigValue[1]
            if lambda1[i,j] > 120 and lambda2[i,j] > 120:
                markArr[i,j] = 1
    return markArr

#  create a function to draw the corners which is detected by former algorithms 
def drawCircleOnImg(Img, markArr):
    Img = Img.convert('RGB')
    draw = ImageDraw.Draw(Img)
    count = 0
    for i in range(markArr.shape[0]):
        for j in range(markArr.shape[1]):
            if markArr[i, j] > 0:
                draw.ellipse( (j - 2, i - 2, j + 2, i + 2), outline ='orange')
                count = count + 1
    print( "total circle drawing : " + str(count) )
    Img.show()   
    
# main function to implement other functions    
def main(imgPath):
    Img = Image.open(imgPath).convert('L')
    mark = hessianCornerDetection(Img)   
    drawCircleOnImg(Img,mark)
      
main('input1.png')