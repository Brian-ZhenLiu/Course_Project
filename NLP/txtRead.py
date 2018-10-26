
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
                           wordsList.append('\n')
                        else:
                            wordsList.append(temp[i])
                    else:
                        wordsList.append(temp[i])
    return wordsList

def generate(path):
    dataList = readFile(path)
    newList = []
    newDataList = normalization(dataList, newList)
    newList = [[]]
    count = 0
    for i in range(len(newDataList)):
        if newDataList[i] != '\n':
            newList[count].append(newDataList[i])
        else:
            newList.append([])
            count = count + 1
    newList.pop()
    return newList
