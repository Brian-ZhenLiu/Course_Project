from skimage import exposure
from skimage import feature
from PIL import Image
from sklearn import svm, metrics
from sklearn.model_selection import cross_val_score, train_test_split, GridSearchCV
import argparse
import numpy as np
import pandas as pd
import os
import glob
import time
# reorgnize the dataset and output a img list and a ground truth list
def getFilePath(path):
    imgPathList = []
    txtPathList = []
    
    for filename in os.listdir(path):
        if filename == "ucf action":
            path = path + "/ucf action"
            for actionFileName in os.listdir(path):

                if (actionFileName != "Golf-Swing-Back" and 
                    actionFileName != ".DS_Store" and 
                    actionFileName != "Golf-Swing-Front"):
                    subPath = path + "/" + actionFileName
                    for splitFileNum in os.listdir(subPath):
                        imagePath = subPath + "/" + splitFileNum
                        try:
                            os.listdir(imagePath + "/gt")
                        except IOError:
                            print(imagePath + " doesn't have gt file to crop image")
                        else:
                            for splitImageFile in os.listdir(imagePath):
                                if os.path.splitext(splitImageFile)[-1] == ".jpg":
                                    imgPathList.append(imagePath + "/" + splitImageFile)
                                if splitImageFile == "gt":
                                    gtPath = imagePath + "/gt"
                                    for splitImageGTFile in glob.glob(os.path.join(gtPath, '*.txt')):
                                        txtPathList.append(splitImageGTFile)
                        
    return imgPathList, txtPathList
# using HoG to get features of all image
def HoG(imgPathList, txtPathList, size, binNum, cell, block):
    print("doing hog for all image in dataset .........")
    Y = []
    X = []
    start_time = time.time()
    count = 0
    # get crop position, crop the image and rezize it 
    while len(imgPathList) != 0 or len(txtPathList) != 0:
        path = imgPathList.pop()
        img = Image.open(path).convert('L')
        file = open(txtPathList.pop(), "r")
        temp = file.read().split("\t")
        # get crop position
        x = (int)(temp[0])
        y = (int)(temp[1])
        u = (int)(temp[2])
        v = (int)(temp[3])
        if(u == 0 or v == 0):
            continue
        Y.append(temp[4])
        # crop image to the region we want
        img = img.crop((x, y, x + u, y + v))
        # resize the image to the given size
        img = img.resize(size)
        # get HoG features in given cells and blocks and using L2 regulazition to every block
        HoG = feature.hog(img, orientations=binNum, pixels_per_cell=cell, 
            cells_per_block=block, block_norm="L2", transform_sqrt=True, visualise=False)

        X.append(HoG.tolist())
        file.close()
        img.close()
    end_time = time.time()
    print("doing hog took :", str(end_time - start_time))
    return X, Y
# using GridSearch function to implement svm to make the classification 
def svcGridSearch(XTrains, XTests, YTrains, YTests, k):
    print("training model by using SVC")
    start_time = time.time()
    # set penalty cost grid for getting the best cost penalty
    paramGrid=[
                 { 
                 "C":[ 0.01, 0.1, 0.5, 1, 1.5, 2] },
                  ]
    # build model by using linear kernel and one vs one as the desision function
    svc = svm.SVC(kernel="linear", decision_function_shape="ovo")
    # doing k-fold cross validation
    grid = GridSearchCV(svc, param_grid=paramGrid, cv=k, n_jobs=-1)
    # trainning svm
    grid.fit(XTrains, YTrains)
    end_time = time.time()
    print("training model took :", str(end_time - start_time))
    return grid

def SVC(X, Y, k):
    X = np.array(X)
    Y = np.array(Y).flatten()
    # split dataset into trainning and testing set
    XTrains, XTests, YTrains, YTests = train_test_split(X, Y, test_size=0.3, random_state=1)
    # doing test 
    grid = svcGridSearch(XTrains, XTests, YTrains, YTests, k)

    return grid.best_score_, grid.best_estimator_.C, metrics.accuracy_score(YTests, grid.predict(XTests))

# get image and ground truth txt list
imgPathList, txtPathList = getFilePath("ucf_sports_actions")

# doing HoG
X, Y = HoG(imgPathList, txtPathList, (64, 128), 9, (8,8), (2,2))

# doing svm for classification
validationScore, bestC, accuracy = SVC(X, Y, 5)
# print output
print("Using linear Kernel " + ", which Best parameter C=" + str(bestC) + " , validation score= "
       + str(validationScore) +  ", Accuracy score=" + str(accuracy) )