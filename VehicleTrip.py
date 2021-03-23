from LineSegment import LineSegment


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

    def getLineSegments(self):
        for index, point in enumerate(self.partitionpoints ):
            if index < len(self.partitionpoints ) -1:
                l1 = LineSegment(self.partitionpoints[index], self.partitionpoints[index+1],index, self.id, self.index)
                self.LineSegments.append(l1)
        return  self.LineSegments