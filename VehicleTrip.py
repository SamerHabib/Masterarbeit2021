from Distance import Point2Point
from LineSegment import LineSegment
import matplotlib.pyplot as plt


class VehicleTrip:
    def __init__(self):
        self.id = None
        self.index = None
        self.orgin = None
        self.end = None
        self.orginId = None
        self.endId = None
        self.points = None
        self.partitionpoints = []
        self.LineSegments = []
        self.distance = None

    def getLineSegments(self):
        for index, point in enumerate(self.partitionpoints ):
            if index < len(self.partitionpoints ) -1:
                l1 = LineSegment(self.partitionpoints[index], self.partitionpoints[index+1],index, self.id, self.index)
                self.LineSegments.append(l1)
        return  self.LineSegments

    def calcDistance(self):
        startIndex = 0
        currentIndex = 1
        self.distance = 0
        while currentIndex < len(self.partitionpoints):
            self.distance += Point2Point(self.partitionpoints[startIndex], self.partitionpoints[currentIndex], True)
            startIndex = currentIndex
            currentIndex += 1

    def drLines(self):
        x = []
        y = []
        for p in self.points:
            x.append(p[0])
            y.append(p[1])
        plt.plot(x, y)
        plt.scatter(x, y)
        plt.show()

    def parLines(self):
        x = []
        y = []
        for p in self.partitionpoints:
            x.append(p[0])
            y.append(p[1])
        plt.plot(x, y)
        plt.scatter(x, y)
        plt.show()