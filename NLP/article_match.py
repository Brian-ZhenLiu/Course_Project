# There are two arguments needed to input in the command line:
# 1. src txt path as a string type (--srcDir)
# 2. tgt txt path as a string type (--tgtDir)

import numpy as np
from numpy import*
import argparse

def sbLabel(src, tgt, table):
    sbTable = []
    firstRow = []
    secRow = []
    for i in range(3):
        if i < 2:
            firstRow.append(" ")
            secRow.append(" ")
        else:
            secRow.append("#")
    for i in range(len(tgt) + 1):
        firstRow.append(i)
    sbTable.append(firstRow)
    for word in tgt:
        secRow.append(word[:3])
    sbTable.append(secRow)
    for i in range(len(src) + 1):
        sbTable.append([])
    sbTable[2].append(0)
    sbTable[2].append("#")
    for i in range(3, len(src) + 3):
        sbTable[i].append(i - 2)
        sbTable[i].append(src[i - 3][:3])
    for i in range(len(table)):
        for j in range(len(table[i])):
            if type(table[i][j]) == np.float64:
                sbTable[i + 2].append(int(table[i][j]))
            else:
                sbTable[i + 2].append(table[i][j])
    for i in range(len(sbTable)):
        # print(sbTable[i])
        temp = ""
        for j in range(len(sbTable[i])):
            if len(str(sbTable[i][j]))== 1:
                temp = temp + str(sbTable[i][j]) + "    "
            elif len(str(sbTable[i][j])) == 2:
                temp = temp + str(sbTable[i][j]) + "   "
            elif len(str(sbTable[i][j])) == 3:
                temp = temp + str(sbTable[i][j]) + "  "
        print(temp)

def traceBack(matchList, s, t, src, tgt, dTable, btTable):
    if btTable[s][t] == "  ":
        return (s, t)
    elif btTable[s][t] == "DI":
        if dTable[s, t] - dTable[s - 1, t - 1] == 2:
            matchList.append((src[s - 1], tgt[t - 1], ' '))
        else:
            matchList.append((src[s - 1], tgt[t - 1], 's'))
        return traceBack(matchList, s - 1, t - 1, src, tgt, dTable, btTable)
    elif btTable[s][t] == "UP":
        matchList.append((src[s - 1], '_', 'd'))
        return traceBack(matchList, s - 1, t, src, tgt, dTable, btTable)
    elif btTable[s][t] == "LT":
        matchList.append(('_', tgt[t - 1], 'i'))
        return traceBack(matchList, s, t - 1, src, tgt, dTable, btTable)

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
    return maxValueCoorList, maxValue

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

def normalization(wordsList, dataLists):
    lowerList = ruleOne(wordsList)
    for word in lowerList:
        r2Word = ruleTwo(word, dataLists)
        if r2Word == "":
            continue
        else:
            r3Word, backSign = ruleThree(r2Word, dataLists)
            ruleFour(r3Word, dataLists)
            if len(backSign) > 0:
                for sign in backSign:
                    dataLists.append(sign)
    return dataLists

def ruleFour(word, dataLists):
    newWord = ""
    charList = list(word)
    if charList[len(charList) - 2] == "'":
        if charList[len(charList) - 1] == "s":
            for i in range(2):
                charList.pop(len(charList) - 1)
            for letter in charList:
                newWord = newWord + letter
            dataLists.append(newWord)
            dataLists.append("'s")
        elif charList[len(charList) - 1] == "t":
            if charList[len(charList) - 3] == "n":
                for i in range(3):
                    charList.pop(len(charList) - 1)
                for letter in charList:
                    newWord = newWord + letter
                dataLists.append(newWord)
                dataLists.append("not")
        elif charList[len(charList) - 1] == "m":
            for i in range(2):
                charList.pop(len(charList) - 1)
            for letter in charList:
                newWord = newWord + letter
            dataLists.append(newWord)
            dataLists.append("am")
    else:
        dataLists.append(word)


def ruleThree(word, dataLists):
    count = 0
    newWord = ""
    backSign = []
    charList = list(word)
    if isAlphanumeric(charList[len(charList) - 1]) == False:
        for i in range(len(charList) - 1, -1, -1):
            if isAlphanumeric(charList[i]) == False:
                count = count + 1
                if isAlphanumeric(charList[i - 1]) == True:
                    break
        for i in range(count, 0, -1):
            backSign.append(charList.pop(len(charList) - i))
    for letter in charList:
        newWord = newWord + letter
    return newWord, backSign

def ruleTwo(word, dataLists):
    count = 0
    newWord = ""
    allSign = ""
    charList = list(word)
    if isAlphanumeric(charList[0]) == False:
        for i in range(len(charList)):
            if isAlphanumeric(charList[i]) == False:
                allSign = allSign + charList[i]
                count = count + 1
                if i == len(charList) - 1:
                    dataLists.append(allSign)
                    break
                elif isAlphanumeric(charList[i + 1]) == True:
                    for sign in list(allSign):
                        dataLists.append(sign)
                    break
        for i in range(count - 1, -1, -1):
            charList.pop(i)
    for letter in charList:
        newWord = newWord + letter
    return newWord

def ruleOne(wordsList):
    newList = []
    for word in wordsList:
        newList.append(word.lower())
    return newList

def isAlphanumeric(letter):
    if 97 <= ord(letter.lower()) <= 122 or 48 <= ord(letter.lower()) <= 57:
        return True
    else:
        return False

def readFile(path):
    wordsList = []
    with open(path, "r") as filestream:
        for line in filestream:
            temp = line.split(" ")
            for i in range(len(temp)):
                if temp[i] == "\n" or temp[i] == "\t" or temp[i] == "":
                    continue
                else:
                    if len(list(temp[i])) >= 2:
                        if temp[i][len(list(temp[i]))-1:] == "\n" or \
                           temp[i][len(list(temp[i]))-1:] == "\t":
                           wordsList.append(temp[i][:len(list(temp[i])) - 1])
                        else:
                            wordsList.append(temp[i])
                    else:
                        wordsList.append(temp[i])
    return wordsList

def main(srcPath, tgtPath):
    print("\nUniversity of Central Florida\nCAP6640 Spring 2018 - Dr. Glinos\nText Similarity Analysis by Zhen Liu\n")
    srcFileName = srcPath.split("/")
    tgtFileName = tgtPath.split("/")
    print("Source file: " + srcFileName[len(srcFileName) - 1])
    print("Target file: " + tgtFileName[len(tgtFileName) - 1])
    print("\nRow Tokens:")
    print("    Source > ", readFile(srcPath))
    print("    Target > ", readFile(tgtPath))

    srcDataLists = []
    tgtDataLists = []
    srcList = readFile(srcPath)
    tgtList = readFile(tgtPath)

    src = normalization(srcList, srcDataLists)
    tgt = normalization(tgtList, tgtDataLists)
    gap = -1
    print("\nNormalized Tokens:")
    print("    Source > ", src)
    print("    Target > ", tgt, "\n")

    dTable = distTable(src, tgt, gap)
    print("Edit Distance Table:\n")
    sbLabel(src, tgt, dTable)

    btTable = backTrTable(src, tgt, dTable)
    print("\nBacktrace Table:\n")
    sbLabel(src, tgt, btTable)

    maxValueCoorList, maxValue = searchMax(src, tgt, dTable)
    print("\nMaximum value in distance table: ", maxValue)
    print("\nMaxima:")
    #print("    ", maxValueCoorList, "\n")
    for i in range(len(maxValueCoorList)):
        print("    ", maxValueCoorList[i])

    print("\nMaximal-similarity alignments:\n")
    order = 0
    for coor in maxValueCoorList:
        matchList = []
        srcAlignList = []
        tgtAlignList = []
        actionList = []
        (sCoor, tCoor) = coor
        (s, t) = traceBack(matchList, sCoor, tCoor, src, tgt, dTable, btTable)
        for pair in matchList:
            (srcPair, tgtPair, action) = pair
            srcAlignList.insert(0, srcPair)
            tgtAlignList.insert(0, tgtPair)
            actionList.insert(0, action)
        print("    Alignment ", order, "(length ", len(srcAlignList), "):")
        print("		Source at ", s, "	:", srcAlignList)
        print("		Source at ", t, "	:", tgtAlignList)
        print("		Edit action	:", actionList)
        order = order + 1

parser = argparse.ArgumentParser('NLProgram1')
parser.add_argument('--srcDir',
					type=str,
					help="Indicate Source file path")
parser.add_argument('--tgtDir',
					type=str,
					help="Indicate Target file path")
FLAG, unparsed = parser.parse_known_args()

if FLAG.srcDir == None or FLAG.tgtDir == None:
	print("Please indicate Source and Target file path.")
else:
	main(FLAG.srcDir, FLAG.tgtDir)
