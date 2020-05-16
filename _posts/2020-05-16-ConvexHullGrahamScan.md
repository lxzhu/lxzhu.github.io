---
title: Convex Hull by Graham's Scan
subtitle: an implementation in Python
tags: [Convex Hull, Graham's Scan, Python]
---

In this post, I implement Graham's Scan algorithm to get convex hull of a list of points. Graham's Scan algorithm contains a step to sort points by reversed polar angles. So a sort algorithm with supporting of customized comparing function is needed. I makde a customized version of [Quick Sort](/2020-05-16-QuickSortInPython){:target="_blank"}

matplotlib is used to show the construction process step by step. It is not the essential part of the algorithm so it is safe to remove all codes relates to plot.

Graham’s Scan computes the convex hull for a collection of Cartesian points. It locates the lowest point, low, in the input set P and sorts the remaining points { P – low } in reverse polar angle with respect to the lowest point. With this order in place, the algorithm can traverse P clockwise from its lowest point. Every left turn of the last three points in the hull being constructed reveals that the last hull point was incorrectly chosen so it can be removed.

```python
#
# author: Liangxiong Zhu
# date: 2020-05-16
# contact: lxzhu@outlook.com
# license: The author does not guarantee the quality of this code. 
#          You take all the responsibilities, not matter good or bad, if you use this code.
#          Keep THIS comment block, then you are licensed.
#

%matplotlib inline
import sys
import math
import matplotlib.pyplot as plt
import QuickSort

class Point:
    def __init__(self,x:int,y:int):
        self.x=x
        self.y=y
    def __str__(self):
        return f'({self.x},{self.y})'
    def __repr__(self):
        return str(self)

class GrahamScan:
    def __init__(self, showPlot:bool=False):
        self.showPlot=showPlot
        
    def computeConvexHull(self, points:[Point]):
        self.plot(points,None)
        lowestPtIndex = self.getLowestPointIndex(points)
        points[lowestPtIndex], points[-1]=points[-1],points[lowestPtIndex]
        lowestPt=points[-1]
        compare=self.makePolarAngleCompare(lowestPt)
        QuickSort.sort(points,low=0,high=len(points)-1,compare=compare,reverse=True)
        self.plot(points,None)
        if self.isCollinear(points,lowestPt):
            return [points[-1],points[0]]
        
        hull=[points[-2],points[-1]]
        
        for pt in points[0:-1]:
            while self.isLeftTurn(hull[-2],hull[-1],pt):
                hull.pop()
            hull.append(pt)
            self.plot(points,hull)
        
        return hull

    def getLowestPointIndex(self,points:[Point]):
        # This is a little special in Python3: integer in Pythopn3 is unbounded. 
        # When integer is unbounded, we can not initialize the minPointX to something like int.MIN_VALUE.
        # 
        # In Python3, it is possible to put any number into an integer no matter how large it is.
        # For example, the largest number of a 64 bits integer is 2^63-1. However, if you put 2^63 into a variable, Python3 will accept it 
        # and handle it correctly. 
        #
        # When a number is too large to be handled by the hardware, Python3 handle it in software.
        minPointY=points[0].y
        minPointIndex=0
        for index in range(len(points)):
            pt=points[index]
            if pt.y<minPointY:
                minPointY=pt.y
                minPointIndex=index
        return minPointIndex
    
    def isLeftTurn(self,pt1:Point,pt2:Point,pt3:Point):
        # based on these three points, we construct two lines (pt1,pt3) and (pt1,pt2)
        # slot(pt1,pt3) is: (pt3.y-pt1.y)/(pt3.x-pt1.x)
        # slot(pt1,pt2) is: (pt2.y-pt1.y)/(pt2.x-pt1.x)
        # when pt1, pt2 and pt3 makes a left turn, line (pt1,pt3) is on the left of line (pt1, pt2)
        # so slot(pt1,pt3)>slot(pt1,pt2)
        # (pt3.y-pt1.y)/(pt3.x-pt1.x) > (pt2.y-pt1.y)/(pt2.x-pt1.x)
        # =>(pt3.y-pt1.y)*(pt2.x-pt1.x)>(pt2.y-pt1.y)*(pt3.x-pt1.x)
        # =>(pt3.y-pt1.y)*(pt2.x-pt1.x)-(pt2.y-pt1.y)*(pt3.x-pt1.x)>0
        
        # it is easier to understand if you translate and rotate axies so that
        # pt1 becomes original point and pt2 is on the positive side of x-axies.
        # after this operation, it is a left turn when pt3.y >0
        return (pt3.y-pt1.y)*(pt2.x-pt1.x)-(pt2.y-pt1.y)*(pt3.x-pt1.x)>0
    
    def makePolarAngleCompare(self,basePt:Point):
        def polarAngleCompare(pt1:Point,pt2:Point):
            if pt1.x==pt2.x and pt1.y==pt2.y:
                return 0
            deltaY1=pt1.y-basePt.y
            deltaX1=pt1.x-basePt.x
            deltaY2=pt2.y-basePt.y
            deltaX2=pt2.x-basePt.x
            angle1=math.atan2(deltaY1, deltaX1)
            angle2=math.atan2(deltaY2, deltaX2)
            if angle1 < angle2:
                return -1
            elif angle1 > angle2:
                return +1
            else:
                if deltaY1 < deltaY2:
                    return -1
                elif deltaY1 > deltaY2:
                    return +1
                else:
                    return 0
            
        return polarAngleCompare
    #
    # if the after sorting by polar angle
    #
    def isCollinear(self,points:[Point], lowPt:Point):
        firstPt=points[0]
        lastPt=points[-2]
        firstAngle=math.atan2(firstPt.y-lowPt.y, firstPt.x-lowPt.x)
        lastAngle=math.atan2(lastPt.y-lowPt.y, lastPt.x-lowPt.x)
        if firstAngle == lastAngle:
            return True
        else:
            return False
    
    def plot(self,points:[Point]=None, hull:[Point]=None):
        if self.showPlot:
            hasPlot=False
            if not points == None:
                plt.plot([e.x for e in points],[e.y for e in points], "o")
                plt.plot([e.x for e in points],[e.y for e in points], "r--")
                hasPlot=True
            if not hull == None:
                plt.plot([e.x for e in hull],[e.y for e in hull],"--",color="blue",linewidth=5 );
                hasPlot=True
            if hasPlot:
                plt.show()
```
