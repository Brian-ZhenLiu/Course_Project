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

def barberAssignment(customers, barberList, barberNum):
    for i in range(len(customers)):
        minIndex = 0
        for j in range(len(barberList)):
            if barberList[j][1] < barberList[minIndex][1]:
                minIndex = j
        barber, money = barberList[minIndex]
        money = money + customers[i]
        barberList[minIndex] = (barber, money)

def main(path, barberNum):
    customers = readInputData(path)
    customers = np.append(customers,np.zeros(barberNum - customers.shape[0]%barberNum))
    barberList = []
    for i in range(barberNum):
        barberList.append([chr(65+i), 0])
    barberAssignment(customers, barberList, barberNum)
    output(barberList)
    
main('testData.txt', 5)    