import numpy as np
import csv

def readInputData(path):
    file = open(path, "r")
    reader = csv.reader(file)
    temp = []
    for row in reader:
        for col in row:
            temp.append(col.split(" "))
    customers = np.array(temp).flatten(order='F')
    customers = customers.astype(np.float)
    return customers

def output(barberList):
    for i in range(len(barberList)):
        print("Barber " + barberList[i][0] + " earned $" + str(barberList[i][1]) + " at the end of day")
        
def barberAssignment(barberList, customers, thres, barberNum):
    for k in range(0, (int)(customers.shape[0] / barberNum)):
        for l in range(barberNum * k, barberNum * k + barberNum):
            barber, money = barberList[l%barberNum]
            money = money + customers[l]
            barberList[l%barberNum] = (barber, money)
        for i in range(len(barberList) - 1):
            for j in range(i, len(barberList)):
                if barberList[i][1] - barberList[j][1] >= thres:
                    barberList.insert(i,barberList.pop(j))    
    return barberList
    
def main(path, barberNum, thres):
    customers = readInputData(path)
    customers = np.append(customers,np.zeros(barberNum - customers.shape[0]%barberNum))
    barberList = []
    for i in range(barberNum):
        barberList.append([chr(65+i), 0])
    barberList = barberAssignment(barberList, customers, thres, barberNum)
    barberList = sorted(barberList, key=lambda BB: BB[0])
    output(barberList)    

main('testData.txt', 5, 20)    
    
    
    
    
