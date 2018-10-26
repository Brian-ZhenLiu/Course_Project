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

def KruskalMST(graph):
    nodesSet = {}
    edgeSet = {}
    allEdgeSet = {}
    allNodesSet = {}
    totalWeight = 0
    nodesSet['AA'] = 'A'
    for i in graph:
        for k in graph[i]:
            temp = (i,k)
            if ord(i) < ord(k):
                allEdgeSet[''.join(temp)] = graph[i][k]
                allNodesSet[''.join(temp)] = k
    unprocessed = allEdgeSet.copy()  
    for i in allEdgeSet:
        # minimum weights' key
        minKey = {v:k for k,v in unprocessed.items()}[min(unprocessed.values())]
        # non-cycle operation
        if allNodesSet[minKey] not in nodesSet.values():
            totalWeight = totalWeight + min(unprocessed.values())
            edgeSet[i] = minKey
            nodesSet[i] = allNodesSet[minKey]
        unprocessed.pop(min(unprocessed,key = unprocessed.get)) 
    edgeList = edgeSet.values()
    nodeList = nodesSet.values()
    print("Minimum Spanning Tress : Total weights on MST edges = %d" %totalWeight)
    print("Node Set = { %s } , Edge Set = { %s }" %(nodeList, edgeList) )
    
        
KruskalMST(G)