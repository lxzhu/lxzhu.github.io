---
title: Quick sort in Python
subtitle: support comparing function
tags: [Python, Quick Sort, Algorithm]
---

This is a part of Python learning process.

I would like to write Graham's Scan algorithm to compute convex hull in Python. There is a step to sort points by reversed polar angles. The builtin sort method in Python supports a key function to extract key from element, then comparing elements by key. It is not enough to implement Graham's Scan algorithm. Parameter compare is added to support comparing two elements in any way the user would like to instead of just by key. 

The main process of quick sort is a divide and conquer strategy. The algorithm divid the input into (left part, pivot element, right part) three parts. During the dividing, the algorithm move elements to make sure that all elements in left part are less than pivot element, while all elements in right part are great than or equals the pivot element. Then the algorithm do the same thing for the left part and right part recursively until the left part and right part becomes single element.



```Python
#
# author: Liangxiong Zhu
# date: 2020-05-16
# contact: lxzhu@outlook.com
# license: The author does not guarantee the quality of this code. 
#.         You take all the responsibilities, not matter good or bad, if you use this code.
#          Keep THIS comment block, then you are licensed.
#

# This is a part of Python learning process.
#
# I would like to write Graham's Scan algorithm to compute convex hull in Python.
# There is a step to sort points by reversed polar angles.
# The builtin sort method in Python supports a key function to extract key from element.
# It is not enough to implement Graham's Scan algorithm
# 
# Paramter compare is added to support user of this algorithm to compare two elements
# in any way they would like instead of just by comparing key. 

# Comparing by key is supported as well.

class QuickSort:
    
    @staticmethod
    def sort(items,low:int=None,high:int=None,compare=None,key=None,reverse=False):
        if low == None or low <0:
            low=0
        if high ==None or high>len(items)-1:
            high=len(items)-1
        if low > high:
            low, high=high, low
        QuickSort.__sort(items,low,high,compare,key,reverse)
        
    @staticmethod
    def __sort(items,low:int,high:int,compare,key,reverse):
        if low<high:
            pi = QuickSort.__partition(items,low,high,compare,key,reverse);
            QuickSort.__sort(items,low,pi-1,compare,key,reverse);
            QuickSort.__sort(items,pi+1,high,compare,key,reverse);
    
    @staticmethod
    def __partition(items,low:int,high:int,compare,key,reverse:bool):
        
        # pick the last element as pivot
        # it does not matter which element is picked as pivot,
        # this partition method must guarentee:
        #   1. returns an index pi inside the range of (low, high).
        #   2. for any x in items[low:pi-1] and any y in items[pi+1,hight], 
        #      exists x<items[pi]<=y
        pivot=items[high]
        
        # index of the last smaller element.
        # the main process of this algorithm is moving elements smaller than pivot to the left side.
        # this index is used to record index of the last smaller elements, 
        # so that we can move the current element to lastSmallerElementIndex+1
        # if current element is less than pivot.
        lastSmallerElementIndex=low-1
        
        # to support comparing by key
        # use the element as key when key function is not provided.
        pivotKey=pivot
        if not key==None:
            pivotKey=key(pivot)
            
        # go through each element in items[low:high]
        # if it is less than the pivot element, 
        #  1. move it to items[lastSmallerElementIndex+1]
        #  2. advance lastSmallerElementIndex a step
        for currentIndex in range(low,high):
            current=items[currentIndex]
            currentKey=current
            if not key==None:
                currentKey=key(current)
                
            isLessThan=False
            
            # if comare is not presented, fallback to ordinary < operator
            if compare == None:
                isLessThan = currentKey < pivotKey
            else:
                isLessThan = compare(currentKey,pivotKey)<0
                
            if reverse == True:
                isLessThan = not isLessThan
                
            if isLessThan:
                items[lastSmallerElementIndex+1],items[currentIndex] = \
                items[currentIndex],items[lastSmallerElementIndex+1]
                lastSmallerElementIndex=lastSmallerElementIndex+1
                
                
        # move the pivot to its correct position
        #
        # range(low, high) is [low, high) which means high is not visited 
        # 
        # after the loop, we are sure that items[low,lastSmallerElementIndex] are less than pivot
        # and items[lastSmallerElementIndex,high-1] are great than or equals to pivot
        #
        # we move the pivot element to lastSmallerElementIndex +1
        # which also means the pivotIndex after moving will be lastSmallerElementIndex+1
        
        # after this step, we are sure that 
        #     for any x in items[low,lastSmallerElementIndex+1-1] 
        #     for any y in items[lastSmallerElementIndex+1+1]
        #     exists x < pivot <= y
        pivotIndex = lastSmallerElementIndex+1
        items[pivotIndex],items[high] = items[high],items[pivotIndex]
        
        return pivotIndex
```

TODO:
Unit tests SHOULD and VERY LIKELY be supplied later.

