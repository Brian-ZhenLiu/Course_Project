import numpy as np
import time

def siftUp(arr, i, size):
    #lc,rc means left,right children 
    lc = 2 * i + 1
    rc = 2 * i + 2
    #index of the largest one in a parent-children system
    maxIndex = i
    if i < size/2:
        #cpmpare children and parent
        if lc < size and arr[lc] > arr[maxIndex]:
            maxIndex = lc
        if rc < size and arr[rc] > arr[maxIndex]:
            maxIndex = rc
        #if an index exchange happened exchange nodes value
        if maxIndex != i:
            arr[maxIndex], arr[i] = arr[i], arr[maxIndex]
            #doing recursive to next level siftup
            siftUp(arr, maxIndex, size)
    return arr

def heapSort(arr):
    size = len(arr)
    #heapify the origin array                      
    for i in range(int(size/2))[::-1]:
        siftUp(arr, i, size)
    print(arr)
    #exchange the root node with the rightmost leaf in the deepest level
    #reheap the new array without changing last changing nodes
    for i in range(size)[::-1]:
        arr[0], arr[i] = arr[i], arr[0]
        siftUp(arr, 0, i)
    return arr

a = np.array([22,9,12,35,4,36,42,65,33,34,18,39,23,30,25,21,19])
print(heapSort(a))        
    