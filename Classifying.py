import math

from Distance import *
from LineSegment import LineSegment
from Plotlib import *


def classifyTheLineSegments(lineSegments):
    allSet = []
    startIndex = 0
    while startIndex < len(lineSegments):
        _set = []
        line1 = lineSegments[startIndex]
        _set.append(line1)
        currentIndex = startIndex + 1
        while currentIndex < len(lineSegments):
            line2 = lineSegments[currentIndex]
            angle = angleLineSegment2LineSegment1(line1.startpoint, line1.endpoint, line2.startpoint, line2.endpoint)
            cosAngle = cosAngleLineSegment2LineSegment(line1.startpoint, line1.endpoint, line2.startpoint, line2.endpoint)
            if cosAngle > math.cos(math.radians(75)):
            #if abs(angle) <= 75:
                valid = checkDistanceBetweenTwoLines(line1, line2)
                if valid:
                    _set.append(line2)
            currentIndex = currentIndex + 1
        startIndex = startIndex + 1
        allSet.append(_set)
    return allSet

def checkDistanceBetweenTwoLines(line1, line2):
    distanceInfo1 = Point2Point(line1.startpoint, line1.endpoint, True)
    distanceInfo2 = Point2Point(line2.startpoint, line2.endpoint, True)

    sortedArr = sorted([(line1.startpoint[0], line1.startpoint[1]), (line2.startpoint[0], line2.startpoint[1])])
    if sortedArr[0] == line1.startpoint:
        distance, m_projectionpoint, m_coefficient  = distancePoint2LineSegment(line1.startpoint, line1.endpoint, line2.startpoint, True)
        parallelDis = Point2Point(line1.startpoint, m_projectionpoint, True)
        if parallelDis > distanceInfo2:
           return False
    else:
        distance, m_projectionpoint, m_coefficient   = distancePoint2LineSegment(line2.startpoint, line2.endpoint, line1.startpoint, True)
        parallelDis = Point2Point(line2.startpoint, m_projectionpoint, True)
        if parallelDis > distanceInfo1:
           return False

    if distanceInfo1 > distanceInfo2:
        perDistance1 = distancePoint2LineSegment(line1.startpoint, line1.endpoint, line2.startpoint)
        perDistance2 = distancePoint2LineSegment(line1.startpoint, line1.endpoint, line2.endpoint)
    else:
        perDistance1 = distancePoint2LineSegment(line2.startpoint, line2.endpoint, line1.startpoint)
        perDistance2 = distancePoint2LineSegment(line2.startpoint, line2.endpoint, line1.endpoint)

    if perDistance1[0] + perDistance2[0] != 0.0:
        perpendicularDistance = ((math.pow(perDistance1[0], 2) + math.pow(perDistance2[0], 2)) / (perDistance1[0] + perDistance2[0]))
    else:
        perpendicularDistance = 0.0

    if(perpendicularDistance > 0):
            return True

def computeScore(set, matrix):
    line1 = set[0]
    currentIndex = 1
    ang1 = angleLineSegment2LineSegment1((0, 1, 0), (1, 1, 0), line1.startpoint, line1.endpoint)
    ang = math.degrees(angleLineSegment2LineSegment((0, 1, 0), (1, 1, 0), line1.startpoint, line1.endpoint))
    while currentIndex < len(set):
        line2 = set[currentIndex]
        currentIndex = currentIndex+1
        arr = [(line1.startpoint), (line1.endpoint), (line2.startpoint), (line2.endpoint)]
        rArr = []
        for p in arr:
            newp = rotate(p, ang)
            rArr.append(newp)
        sortedArr = sorted(rArr)

        sPoint = ((rArr[0][0] + rArr[2][0]) / 2, (rArr[0][1] + rArr[2][1]) / 2, (rArr[0][2] + rArr[2][2]) / 2)
        ePoint = ((rArr[1][0] + rArr[3][0]) / 2, (rArr[1][1] + rArr[3][1]) / 2,  (rArr[1][2] + rArr[3][2]) / 2)
        AVdirVec = LineSegment(sPoint,ePoint, 0, 0, 0)
        d1, m_projectionpoint1, m_coefficient1 = distancePoint2LineSegment(sPoint, ePoint, (sortedArr[1]))
        d2, m_projectionpoint2, m_coefficient2 = distancePoint2LineSegment(sPoint, ePoint, (sortedArr[2]))
        d = Point2Point(m_projectionpoint1, m_projectionpoint2)
        matrix[line1.vIndex][line2.vIndex] += d

def rotate(point, ang):
    xc, yc, zc = point
    if ang >= 0 and ang <= 90:
        angle = math.radians(ang)
    elif ang > 90 and ang <= 180:
        angle = math.radians(180 - ang)
    elif ang > 180 and ang <= 270:
        angle = math.radians(ang - 180)
    else:
        angle = math.radians(360 - ang)
    x = (math.cos(angle) * point[0]) +  (math.sin(angle) * point[1])
    y = (-1 * math.sin(angle) * point[0]) + (math.cos(angle) * point[1])
    z = zc
    newpoint = (x, y, z)
    return  newpoint