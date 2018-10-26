import numpy as np
from numpy import*
import argparse
import txtRead

def markovViterbi(initProb, transPTable, emissProbHash, testList):

    results = []
    results.append({})
    results[0][testList[0]] = {}
    if lemmatize([testList[0]])[0] in emissProbHash:
        for key in emissProbHash[lemmatize([testList[0]])[0]]:
            results[0][testList[0]][key] = (emissProbHash[lemmatize([testList[0]])[0]][key] * initProb[key], "null")
    else:
        results[0][testList[0]]['NN'] = 1.000000

    for i in range(1, len(testList)):
        results.append({})
        results[i][testList[i]] = {}
        if lemmatize([testList[i]])[0] in emissProbHash:
            for key in emissProbHash[lemmatize([testList[i]])[0]]:
                results[i][testList[i]][key] = (0, "null")

                for pastKey in results[i - 1][testList[i - 1]]:
                    if (key in transPTable[pastKey]) == False:
                        transPTable[pastKey][key] = 0
                    if results[i][testList[i]][key][0] < emissProbHash[lemmatize([testList[i]])[0]][key] * transPTable[pastKey][key] * results[i - 1][testList[i - 1]][pastKey][0]:
                        results[i][testList[i]][key] = (emissProbHash[lemmatize([testList[i]])[0]][key] * transPTable[pastKey][key] * results[i - 1][testList[i - 1]][pastKey][0], pastKey)

        else:
            results[i][testList[i]]['NN'] = (1.000000, " ")
            # write down something
            temp = 0
            for pastKey in results[i - 1][testList[i - 1]]:
                if "NN" in transPTable[pastKey]:
                    if temp < transPTable[pastKey]["NN"] * results[i - 1][testList[i - 1]][pastKey][0]:
                        results[i][testList[i]]["NN"] = (results[i][testList[i]]["NN"][0], pastKey)
                else:
                    if temp < 0:
                        results[i][testList[i]]["NN"] = (results[i][testList[i]]["NN"][0], pastKey)

    for i in range(len(results)):
        for key in results[i]:
            temp = 0
            for subKey in results[i][key]:
                temp = temp + results[i][key][subKey][0]
            for subKey in results[i][key]:
                results[i][key][subKey] = (results[i][key][subKey][0] / temp, results[i][key][subKey][1])
    return results

def transProbTable(transTable):
    hashTable = transTable.copy()
    for key in hashTable:
        denominator = 0
        count = 0
        for subKey in hashTable[key]:
            denominator = denominator + hashTable[key][subKey]
        for subKey in hashTable[key]:
            hashTable[key][subKey] = float('%.6f' % (hashTable[key][subKey] / denominator))
            count = count + hashTable[key][subKey]
    return hashTable


def generateHashtable(tagList, wordsList):
    transTable = {}
    tagSumTable = {}
    emissProbHash = {}
    count = 0
    for i in range(len(tagList) - 1):
        if (tagList[i] in tagSumTable) == False:
            tagSumTable[tagList[i]] = 1
        else:
            tagSumTable[tagList[i]] = tagSumTable[tagList[i]] + 1

        if (tagList[i] in transTable) == False:
            transTable[tagList[i]] = {}
        if tagList[i + 1] in transTable[tagList[i]]:
            transTable[tagList[i]][tagList[i + 1]] = transTable[tagList[i]][tagList[i + 1]] + 1
        else:
            transTable[tagList[i]][tagList[i + 1]] = 1

        if (wordsList[i] in emissProbHash) == False:
            count = count + 1
            emissProbHash[wordsList[i]] = {}
        if (tagList[i] in emissProbHash[wordsList[i]]) == False:
            emissProbHash[wordsList[i]][tagList[i]] = 1
        else:
            emissProbHash[wordsList[i]][tagList[i]] = emissProbHash[wordsList[i]][tagList[i]] + 1

    for key in emissProbHash:
        for subKey in emissProbHash[key]:
            emissProbHash[key][subKey] = emissProbHash[key][subKey] / tagSumTable[subKey]

    return transTable, emissProbHash

def lemmatize(wordsList):
    newList = []
    for word in wordsList:
        if word[-4:] == 'sses' or word[-3:] == 'xes':
            charList = list(word)
            charList.pop(len(charList) - 1)
            charList.pop(len(charList) - 1)
            newList.append(''.join(charList))

        elif word[-3:] == 'ses' or word[-3:] == 'zes':
            charList = list(word)
            charList.pop(len(charList) - 1)
            newList.append(''.join(charList))

        elif word[-4:] == 'ches' or word[-4:] == 'shes':
            charList = list(word)
            charList.pop(len(charList) - 1)
            charList.pop(len(charList) - 1)
            newList.append(''.join(charList))

        elif word[-3:] == 'men' :
            charList = list(word)
            charList[len(charList) - 2] = 'a'
            newList.append(''.join(charList))

        elif word[-3:] == 'ies':
            charList = list(word)
            charList.pop(len(charList) - 1)
            charList.pop(len(charList) - 1)
            charList[len(charList) - 1] = 'y'
            newList.append(''.join(charList))

        else:
            newList.append(word)

    return newList

def tagSplit(corpusList):
    wordsList = []
    tagList = []
    for i in range(len(corpusList)):
        if i % 2 == 0:
            wordsList.append(corpusList[i].lower())
        if i % 2 == 1:
            tagList.append(corpusList[i])
    return wordsList, tagList

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
                    else:
                        dataList.append(temp[i])
    return dataList

def main(corpusPath, testPath):
    print("\nUniversity of Central Florida\nCAP6640 Spring 2018 - Dr. Glinos\nText Similarity Analysis by Zhen Liu\n")
    print("Viterbi Algorithm HMM Tagger by Zhen Liu\n\n")

    corpusList = readFile(corpusPath)
    wordsList, tagList = tagSplit(corpusList)
    transTable, emissProbHash = generateHashtable(tagList, lemmatize(wordsList))

    print("ALl Tags Observed:\n")
    transPTable = transProbTable(transTable)
    initProb = transPTable[' ']
    count = 1
    for key in sorted(transTable):
        if key != " ":
            print(str(count) + " " + str(key))
            count = count + 1

    print("\nInitial Distribution:\n")
    for key in sorted(initProb):
        print("start [ " + key + " |  ]" + str(initProb[key]))

    print("\nEmission Probabilities:\n")

    for key in sorted(emissProbHash):
        for subKey in sorted(emissProbHash[key]):
            print(str("%+30s" % key ) + "  " + subKey + " " + str(float('%.6f' % emissProbHash[key][subKey])))

    print("\nTransition Probabilities:\n")
    for key in sorted(transPTable):
        count = 0
        temp = ""
        for subKey in sorted(transPTable[key]):
            count = count + transPTable[key][subKey]
            temp = temp + "[" + subKey + "|" + key + "] " + str(transPTable[key][subKey]) + "  "
        print("[ " + str(float('%.6f' % count)) + " ]   " + temp)

    print("\nCorpus Features:\n")
    count = 0
    for key in sorted(transTable):
        if key != " ":
            count = count + 1
    print("  Total # tags        : " + str(count))

    bigrams = 0
    for key in transTable:
        for key2 in transTable[key]:
            bigrams = bigrams + 1
    print("  Total # bigrams     : " + str(bigrams))

    lexicals = 0
    for key in emissProbHash:
        if key != ' ':
            lexicals = lexicals + 1
    print("  Total # lexicals    : " + str(lexicals))

    sentence = 0
    for word in wordsList:
        if word == ' ':
            sentence = sentence + 1
    print("  Total # sentences   : " + str(sentence))

    allTestLists = txtRead.generate(testPath)
    print("\n\nTest Set Tokens Found in Corpus:\n")
    for i in range(len(allTestLists)):
        for j in range(len(allTestLists[i])):
            temp = str( ("%+20s" + " : ") % allTestLists[i][j] )
            if lemmatize([allTestLists[i][j]])[0] in emissProbHash:
                for key in emissProbHash[lemmatize([allTestLists[i][j]])[0]]:
                    temp = temp + key + " (" + str(float('%.6f' % emissProbHash[lemmatize([allTestLists[i][j]])[0]][key])) + ") "
                print(temp)
            else:
                print(  str( ("%+20s" + " : ") % allTestLists[i][j] ) + "NN (1.000000)" )
        print("")


    print("\n\nIntermediate Results of Viterbi Algorithm:\n")
    print(allTestLists)
    for testList in allTestLists:
        results = markovViterbi(initProb, transPTable, emissProbHash, testList)
        count = 0
        for i in range(len(results)):
            count = count + 1
            for key in results[i]:
                temp = ""
                for subKey in results[i][key]:
                    temp = temp + subKey + " (" + str(float('%.6f' % results[i][key][subKey][0])) + ", " + results[i][key][subKey][1] + ") "
                print("Iteration  " + str(count) + " :" +str("%+20s" % key) + " :   " + temp)
        print("")

    print("\n\nViterbi Tagger Output:\n")
    for testList in allTestLists:
        results = markovViterbi(initProb, transPTable, emissProbHash, testList)
        for i in range(len(results)):
            for key in results[i]:
                tag = ""
                prob = 0
                for subKey in results[i][key]:
                    if results[i][key][subKey][0] > prob:
                        prob = results[i][key][subKey][0]
                        tag = subKey

                print(str("%+20s" % key) + "     " + tag)
        print("")


parser = argparse.ArgumentParser('NLProgram2')
parser.add_argument('--trainDir',
					type=str,
					help="Indicate train file path")
parser.add_argument('--testDir',
					type=str,
					help="Indicate test file path")
FLAG, unparsed = parser.parse_known_args()

if FLAG.trainDir == None or FLAG.testDir == None:
	print("Please indicate train and testfile path.")
else:
	main(FLAG.trainDir, FLAG.testDir)
