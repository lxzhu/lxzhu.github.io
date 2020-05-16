---
title: Quick sort in Python
subtitle: support comparing function
tags: [Python, Quick Sort, Algorithm]
---

This is a part of Python learning process.

I would like to write Graham's Scan algorithm to compute convex hull in Python. There is a step to sort points by reversed polar angles. The builtin sort method in Python supports a key function to extract key from element. It is not enough to implement Graham's Scan algorithm. Paramter compare is added to support user of this algorithm to compare two elements in any way they would like instead of just by comparing key. 

```Python
#
# author: Liangxiong Zhu
# date: 2020-05-16
# contact: lxzhu@outlook.com
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
    def sort(items,compare=None,key=None,reverse=False):
        if len(items)<=1:
            return;
        QuickSort.__sort(items,0,len(items)-1,compare,key,reverse);
    
    @staticmethod
    def __sort(items,low:int,high:int,compare,key,reverse):
        if low<high:
            pi = QuickSort.__partition(items,low,high,compare,key,reverse);
            QuickSort.__sort(items,low,pi-1,compare,key,reverse);
            QuickSort.__sort(items,pi+1,high,compare,key,reverse);
        
    #
    # this method take last element as pivot
    #
    @staticmethod
    def __partition(items,low:int,high:int,compare,key,reverse:bool):
        
        # pick the last element as pivot
        # it does not matter which element is picked as pivot,
        # this partition method must guarentee:
        #   1. returns an index pi inside the range of (low, high).
        #   2. for any x in items[low:pi-1] and any y in items[pi+1,hight], 
        #      exists x<=items[pi]<y
        pivot=items[high]
        
        # index of the last smaller element.
        # the main process of this algorithm is moving elements smaller than pivot to the left side.
        # this index is used to record index of the last smaller elements, 
        # so that we can move the current element to lastSmallerElementIndex+1
        # if current element is less than pivot.
        lastSmallerElementIndex=low-1
        
        # to support comparing by key
        pivotKey=pivot
        if not key==None:
            pivotKey=key(pivot)
            
        
        for currentIndex in range(low,high):
            current=items[currentIndex]
            currentKey=current
            if not key==None:
                currentKey=key(current)
                
            isLessThan=False
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
                
                
        # i+1 is the         
        items[lastSmallerElementIndex+1],items[high]=items[high],items[lastSmallerElementIndex+1]
        return lastSmallerElementIndex+1
```
