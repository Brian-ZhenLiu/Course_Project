import csv

def graph(file):
    ifile = open(file, "r")
    reader = csv.reader(ifile)
    dataLists = []
    graph = {}
    for row in reader:
        for col in row:
            temp = col.split(" ")
            dataLists.append(temp)

    for i in range(len(dataLists)):
        for j in range(len(dataLists[i])):
            if j != 0 and j % 2 == 0:
                dataLists[i][j] = (int)(dataLists[i][j])
                #print(dataLists)
    for i in range(len(dataLists)):
        vertex = dataLists[i].pop(0)
        graph[vertex] = {}
        for j in range(len(dataLists[i])):
            if j % 2 == 0: 
                adjVertex = dataLists[i][j]
            if j % 2 != 0:
                graph[vertex][adjVertex] = dataLists[i][j] 
    return graph

G = graph("data.txt")

def dijkstra(graph):
    letters = ['B','C','D','E','F','G','H','I']
    distance = {}
    tempSet = {}
    path = {}
    distance = dict.fromkeys(['B','C','D','E','F','G','H','I'],float('inf'))
    distance['A'] = 0

    for i in graph:
        unprocessed = distance.copy()
        unprocessed.pop(min(unprocessed,key = unprocessed.get)) 
        minKey = {v:k for k,v in unprocessed.items()}[min(unprocessed.values())]
        for k in unprocessed:
            if k in graph[i]:
                if distance[k] > distance[i] + graph[i][k]:
                    distance[k] = distance[i] + graph[i][k]
                    path[k] = i + k
                else:
                    distance[k] = distance[k]   
    
    pathStrLists = []
    for i in range(len(letters)):
        tempStr = letters[i]
        pathStr = tempStr
        while(path.get( tempStr )[0] != 'A'):
            tempStr = path.get( tempStr )[0]
            pathStr = pathStr + tempStr
        pathStrLists.append(pathStr)
    #print(pathStrLists[0][0])
    for i in range(len(pathStrLists) ):
        finalStr = "Destination Node " + pathStrLists[i][0] + " : path value = " + str(distance.get(pathStrLists[i][0])) + ", path is: A"
        for j in range( len(pathStrLists[i])-1, -1, -1 ):
            finalStr = finalStr + " -> " + pathStrLists[i][j]
        print(finalStr)

dijkstra(G)
