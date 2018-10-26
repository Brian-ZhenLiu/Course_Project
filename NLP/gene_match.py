import numpy as np
from numpy import*
import csv

def traceBack(matchList, s, t, src, tgt, dTable, btTable):
    if btTable[s][t] == "  ":
        return
    #print(str(s) + ", " + str(t))
    if btTable[s][t] == "DI":
        traceBack(matchList, s - 1, t - 1, src, tgt, dTable, btTable)
        #if dTable[s, t] - dTable[s - 1, t - 1] == 2:
        matchList.insert(0, (src[s - 1], tgt[t - 1]))

    elif btTable[s][t] == "UP":
        traceBack(matchList, s - 1, t, src, tgt, dTable, btTable)
        matchList.insert(0, (src[s - 1], '_'))
    elif  btTable[s][t] == "LT":
        traceBack(matchList, s, t - 1, src, tgt, dTable, btTable)
        matchList.insert(0, ('_', tgt[t - 1]))


def backTrTable(src, tgt, dTable):
    btTable = []
    for i in range(len(src) + 1):
        btTable.append([])
    for i in range(len(src), 0, -1):
        for j in range(len(tgt), 0, -1):
            if dTable[i, j] == 0:
                btTable[i].insert(0, ("  "))
            else:
                if src[i - 1] == tgt[j - 1]:
                    if dTable[i, j - 1] > dTable[i - 1, j] and dTable[i, j - 1] > dTable[i - 1, j - 1] and dTable[i, j - 1] > dTable[i, j]:
                        btTable[i].insert(0, ("LT"))
                    elif dTable[i - 1, j] > dTable[i, j - 1] and dTable[i - 1, j] > dTable[i - 1, j - 1] and dTable[i - 1, j] > dTable[i, j]:
                        btTable[i].insert(0, ("UP"))
                    else:
                        btTable[i].insert(0, ("DI"))
                else:
                    if dTable[i, j] == dTable[i, j - 1] and dTable[i, j] == dTable[i - 1, j]:
                        btTable[i].insert(0, ("DI"))
                    else:
                        if dTable[i, j - 1] > dTable[i - 1, j]:
                            btTable[i].insert(0, ("LT"))
                        else:
                            btTable[i].insert(0, ("UP"))

    for i in range(len(tgt) + 1):
        btTable[0].insert(0, "  ")
    for j in range(1, len(src) + 1):
        btTable[j].insert(0, "  ")

    return btTable

def searchMax(src, tgt, dTable):
    maxValue = 0
    maxValueCoorList = []
    for i in range(1, len(src) + 1):
        for j in range(1, len(tgt) + 1):
            if dTable[i, j] > maxValue:
                del maxValueCoorList[:]
                maxValue = dTable[i, j]
                maxValueCoorList.append((i, j))
            elif dTable[i, j] == maxValue:
                maxValueCoorList.append((i, j))
    return maxValueCoorList

def distTable(src, tgt, gap):
    dTable = np.zeros((len(src) + 1, len(tgt) + 1))
    for i in range(1, len(src) + 1):
        for j in range(1, len(tgt) + 1):
            dTable[i, j] = max(0,
                               dTable[i - 1, j] + gap,
                               dTable[i, j - 1] + gap,
                               dTable[i - 1, j - 1] + match(src[i - 1], tgt[j - 1]))
    return dTable

def match(letterA,letterB):
    if letterA == letterB:
        return 2
    else:
        return -1

def normalizedToken(txtList):
    for i in range(len(txtList)):
        txtList[i] = txtList[i].lower()
    return txtList

def readFile(path):
    ifile = open(path, "r")
    reader = csv.reader(ifile)
    dataLists = []
    for row in reader:
        for col in row:
            letter = col.split(" ")
            lowerLetter = normalizedToken(letter)
            for i in range(len(lowerLetter)):
                dataLists.append(lowerLetter[i])
    return dataLists

def main(srcPath, tgtPath):
    gap = -1
    src = readFile(srcPath)
    tgt = readFile(tgtPath)

    dTable = distTable(src, tgt, gap)
    maxValueCoorList = searchMax(src, tgt, dTable)
    btTable = backTrTable(src, tgt, dTable)

    matchList = []

    print(maxValueCoorList)
    #print(dTable)
    #for i in range(len(btTable)):
    #    print(str(i) + str(btTable[i]))
    traceBack(matchList, 11, 17, src, tgt, dTable, btTable)
    print(matchList)


main("gene-src.txt", "gene-tgt.txt")
