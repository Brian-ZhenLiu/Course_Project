# There is one argument needed to input in the command line:
# 1. test txt path as a string type (--testDir), for example, --testDir hearing.txt

from numpy import *
import argparse

def oracle(stack, buff, leftArc, rightArc, fullList, fullStack):
    if  len(stack) == 1 and len(buff) == 0:
        print(str(stack) + " " + str(buff) + " ROOT --> " + stack[0])
        return stack
    if len(stack) < 2 and len(buff) > 0:
        shift(stack, buff, fullStack, fullList)
        oracle(stack, buff, leftArc, rightArc, fullList, fullStack)
    else:
        if list(stack)[len(stack) - 2][0] == 'V' and (list(stack)[len(stack) - 1][0] == 'R' or list(stack)[len(stack) - 1][0] == '.'):
            right_arc(stack, buff, fullStack, fullList)
            oracle(stack, buff, leftArc, rightArc, fullList, fullStack)
        elif len(stack) > 2 and list(stack)[len(stack) - 2][0] == 'I' and list(stack)[len(stack) - 1][0] == '.':
                swap(stack, buff, fullStack, fullList)
                oracle(stack, buff, leftArc, rightArc, fullList, fullStack)
        elif (list(stack)[len(stack) - 2][0] == 'V' or\
              list(stack)[len(stack) - 2][0] == 'I') and\
             (list(stack)[len(stack) - 1][0] == 'D' or\
               list(stack)[len(stack) - 1][0] == 'I' or\
               list(stack)[len(stack) - 1][0] == 'J' or\
               list(stack)[len(stack) - 1][0] == 'P' or\
               list(stack)[len(stack) - 1][0] == 'R') and\
               len(buff) != 0:
                shift(stack, buff, fullStack, fullList)
                oracle(stack, buff, leftArc, rightArc, fullList, fullStack)
        else:
            if (stack[len(stack) - 1] in leftArc[stack[len(stack) - 2]]) and (stack[len(stack) - 1] not in rightArc[stack[len(stack) - 2]]):
                left_arc(stack, buff, fullStack, fullList)
                oracle(stack, buff, leftArc, rightArc, fullList, fullStack)
            elif (stack[len(stack) - 1] not in leftArc[stack[len(stack) - 2]]) and (stack[len(stack) - 1] in rightArc[stack[len(stack) - 2]]):
                right_arc(stack, buff, fullStack, fullList)
                oracle(stack, buff, leftArc, rightArc, fullList, fullStack)
            elif(stack[len(stack) - 1] not in leftArc[stack[len(stack) - 2]]) and (stack[len(stack) - 1] not in rightArc[stack[len(stack) - 2]]) and len(buff) != 0:
                shift(stack, buff, fullStack, fullList)
                oracle(stack, buff, leftArc, rightArc, fullList, fullStack)
            else:
                if leftArc[stack[len(stack) - 2]][stack[len(stack) - 1]] >= rightArc[stack[len(stack) -2 ]][stack[len(stack) - 2]]:
                    left_arc(stack, buff, fullStack, fullList)
                    oracle(stack, buff, leftArc, rightArc, fullList, fullStack)
                else:
                    right_arc(stack, buff, fullStack, fullList)
                    oracle(stack, buff, leftArc, rightArc, fullList, fullStack)

def shift(stack, buff, fullStack, fullList):
    print(str(fullStack) + " " + str(fullList) + " SHIFT")
    stack.append(buff.pop(0))
    fullStack.append(fullList.pop(0))

def right_arc(stack, buff, fullStack, fullList):
    temp = str(fullStack) + " " + str(fullList) + " Right-Arc: "
    depend = fullStack.pop(len(fullStack) - 1)
    stack.pop(len(stack) - 1)
    print(temp + fullStack[len(fullStack) - 1] + " --> " + depend)

def left_arc(stack, buff, fullStack, fullList):
    temp = str(fullStack) + " " + str(fullList) + " Left-Arc: "
    depend = fullStack.pop(len(fullStack) - 2)
    stack.pop(len(stack) - 2)
    print(temp + depend + " <-- " + fullStack[len(fullStack) - 1])

def swap(stack, buff, fullStack, fullList):
    print(str(fullStack) + " " + str(fullList) + " SWAP")
    buff.insert(0, stack.pop(len(stack) - 2))
    fullList.insert(0, fullStack.pop(len(fullStack) - 2))


def arcConfusion(leftArc, rightArc):
    confusion = {}
    for key in leftArc:
        confusion[key] = {}
        for subkey in leftArc[key]:
            if subkey in rightArc[key]:
                confusion[key][subkey] = (leftArc[key][subkey], rightArc[key][subkey])
    return confusion

def arcCount(indexList, tagList, headIndexList):
    leftArc = {}
    rightArc = {}
    for i in range(len(tagList)):
        for j in range(len(tagList[i])):
            if int(headIndexList[i][j]) != 0:
                if (tagList[i][j] in leftArc) == False:
                    leftArc[tagList[i][j]] = {}
                if int(headIndexList[i][j]) > int(indexList[i][j]):
                    if tagList[i][int(headIndexList[i][j]) - 1] in leftArc[tagList[i][j]]:
                        leftArc[tagList[i][j]][tagList[i][int(headIndexList[i][j]) - 1]] = leftArc[tagList[i][j]][tagList[i][int(headIndexList[i][j]) - 1]] + 1
                    else:
                        leftArc[tagList[i][j]][tagList[i][int(headIndexList[i][j]) - 1]] = 1

                if (tagList[i][j] in rightArc) == False:
                    rightArc[tagList[i][j]] = {}
                if int(headIndexList[i][j]) < int(indexList[i][j]):
                    if tagList[i][int(headIndexList[i][j]) - 1] in rightArc[tagList[i][j]]:
                        rightArc[tagList[i][j]][tagList[i][int(headIndexList[i][j]) - 1]] = rightArc[tagList[i][j]][tagList[i][int(headIndexList[i][j]) - 1]] + 1
                    else:
                        rightArc[tagList[i][j]][tagList[i][int(headIndexList[i][j]) - 1]] = 1

    return leftArc, rightArc

def listSeperate(dataList):
    indexList = []
    wordList = []
    tagList = []
    headIndexList = []
    for i in range(len(dataList)):
        if i % 4 == 0:
            indexList.append(dataList[i])
        elif i % 4 == 1:
            wordList.append(dataList[i])
        elif i % 4 == 2:
            tagList.append(dataList[i])
        elif i % 4 == 3:
            headIndexList.append(dataList[i])

    indexList = sentenceSplit(indexList)
    wordList = sentenceSplit(wordList)
    tagList = sentenceSplit(tagList)
    headIndexList = sentenceSplit(headIndexList)

    return indexList, wordList, tagList, headIndexList

def sentenceSplit(myList):
    newList = [[]]
    count = 0
    for i in range(len(myList)):
        if myList[i] == ' ':
            newList.append([])
            count = count + 1
        else:
            newList[count].append(myList[i])
    return newList

def readTestFile(path):
    dataList = []
    tagList = []
    fullList = []
    with open(path, "r") as filestream:
        for line in filestream:
            word = ''
            if line[len(list(line)) - 1:] == "\n":
                for i in range(len(list(line)) - 1):
                    word = word + list(line)[i]
                fullList.append(word)
            else:
                fullList.append(line)

            temp = line.split("/")
            for i in range(len(temp)):
                if len(list(temp[i])) >= 2:
                    if temp[i][len(list(temp[i]))-1:] == "\n" or \
                       temp[i][len(list(temp[i]))-1:] == "\t":
                       dataList.append(temp[i][:len(list(temp[i])) - 1])
                    else:
                        dataList.append(temp[i])
                else:
                    dataList.append(temp[i])
    for i in range(len(dataList)):
        if i % 2 == 1:
            tagList.append(dataList[i])
    return fullList, tagList

def readFile(path):
    dataList = []
    with open(path, "r") as filestream:
        for line in filestream:
            temp = line.split(" ")
            for i in range(len(temp)):
                if len(list(temp[i])) >= 2:
                    if temp[i][len(list(temp[i]))-1:] == "\n" or \
                       temp[i][len(list(temp[i]))-1:] == "\t":
                       dataList.append(temp[i][:len(list(temp[i])) - 1])
                    else:
                        dataList.append(temp[i])
                else:
                    if temp[i] == "\n":
                        dataList.append(" ")
                        dataList.append(" ")
                        dataList.append(" ")
                        dataList.append(" ")
                    else:
                        dataList.append(temp[i])
    return dataList

def main(testPath):
    print("\nUniversity of Central Florida\nCAP6640 Spring 2018 - Dr. Glinos\nDependency Parser Analysis by Zhen Liu\n")

    dataList = readFile("wsj-clean.txt")
    fullList, testTags = readTestFile(testPath)
    indexList, wordList, tagList, headIndexList = listSeperate(dataList)
    leftArc, rightArc = arcCount(indexList, tagList, headIndexList)

    tokenNum = 0
    for i in range(len(tagList)):
        for j in range(len(tagList[i])):
            tokenNum = tokenNum + 1

    tagNum = 0
    for key in leftArc:
        tagNum = tagNum + 1

    leftArcNum = 0
    for key in leftArc:
        for subkey in leftArc[key]:
            leftArcNum = leftArcNum + leftArc[key][subkey]

    rightArcNum = 0
    for key in rightArc:
        for subkey in rightArc[key]:
            rightArcNum = rightArcNum + rightArc[key][subkey]

    rootNum = 0
    for i in range(len(headIndexList)):
        for j in range(len(headIndexList[i])):
            if int(headIndexList[i][j]) == 0:
                rootNum = rootNum + 1


    print("Corpus Statistics:\n")
    print("     # " + str("%-11s" % 'sentences') + ": " + str("%+5s" % str(len(wordList))))
    print("     # " + str("%-11s" % 'tokens') + ": " + str("%+5s" % str(tokenNum)))
    print("     # " + str("%-11s" % 'POS tags') + ": " + str("%+5s" % str(tagNum)))
    print("     # " + str("%-11s" % 'Left-Arcs') + ": " + str("%+5s" % str(leftArcNum)))
    print("     # " + str("%-11s" % 'Right-Arcs ') + ": " + str("%+5s" % str(rightArcNum)))
    print("     # " + str("%-11s" % 'Root-Arcs') + ": " + str("%+5s" % str(rootNum)))

    print("\nLeft Arc Array Nonzero Counts:\n")
    for key in sorted(leftArc):
        temp = ""
        temp = temp + str("%+5s" % key ) + " : "
        for subkey in sorted(leftArc[key]):
            temp = temp + "[" + str("%+4s" % subkey ) + ",  " + str("%+3s" % str(leftArc[key][subkey])) + "] "
        print(temp)

    print("\nRight Arc Array Nonzero Counts:\n")
    for key in sorted(rightArc):
        temp = ""
        temp = temp + str("%+5s" % key ) + " : "
        for subkey in sorted(rightArc[key]):
            temp = temp + "[" + str("%+4s" % subkey ) + ",  " + str("%+3s" % str(rightArc[key][subkey])) + "] "
        print(temp)

    confusionArc = arcConfusion(leftArc, rightArc)
    print("\nArc Confusion Array:\n")
    count = 0
    for key in sorted(confusionArc):
        temp = ""
        temp = temp + str("%+5s" % key ) + " : "
        for subkey in sorted(confusionArc[key]):
            temp = temp + "[" + str("%+4s" % subkey ) + ",  " + str("%+4s" % str(confusionArc[key][subkey][0])) + "," + str("%+4s" % str(confusionArc[key][subkey][1])) + "] "
            count = count + 1
        print(temp)

    print("\n      Number of confusing arcs = " + str(count)+ "\n")

    print("\nInput Sentences:\n")
    temp = ""
    for fullMark in fullList:
        temp = temp + fullMark + " "
    print(temp)

    print("\n\nParsing Actions and Transitions:\n")
    stack = []
    fullStack = []
    buff = testTags
    oracle(stack, buff, leftArc, rightArc, fullList, fullStack)


parser = argparse.ArgumentParser('NLProgram3')
parser.add_argument('--testDir',
					type=str,
					help="Indicate test file path")
FLAG, unparsed = parser.parse_known_args()

if FLAG.testDir == None:
	print("Please indicate train and testfile path.")
else:
	main(FLAG.testDir)
