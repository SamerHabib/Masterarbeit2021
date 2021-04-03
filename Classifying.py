import math

import numpy

from Distance import *
from LineSegment import LineSegment
from Plotlib import *
import operator


def classifyTheLineSegments(lineSegments, numberOfVehicles):
    allSet = []
    matrixper = numpy.zeros(shape=(numberOfVehicles, numberOfVehicles))
    matrixCount = numpy.zeros(shape=(numberOfVehicles, numberOfVehicles))
    startIndex = 0
    while startIndex < len(lineSegments):
        _set = []
        line1 = lineSegments[startIndex]
        _set.append(line1)
        currentIndex = startIndex + 1
        while currentIndex < len(lineSegments):
            line2 = lineSegments[currentIndex]
            if(line2.vid != line1.vid):
                angle = angleLineSegment2LineSegment1(line1.startpoint, line1.endpoint, line2.startpoint, line2.endpoint)
                cosAngle = cosAngleLineSegment2LineSegment(line1.startpoint, line1.endpoint, line2.startpoint,
                                                           line2.endpoint)
                if cosAngle > math.cos(math.radians(75)):
                    # if abs(angle) <= 75:
                    valid = checkDistanceBetweenTwoLines(line1, line2, matrixper, matrixCount)
                    if valid:
                        _set.append(line2)
            currentIndex = currentIndex + 1
        startIndex = startIndex + 1
        if len(_set) > 1:
            allSet.append(_set)
    matrixper = np.true_divide(matrixper, matrixCount)
    where_are_NaNs = numpy.isnan(matrixper)
    matrixper[where_are_NaNs] = 0
    matrixper = symmetrize(matrixper)
    return allSet, matrixper


def checkDistanceBetweenTwoLines(line1, line2, matrixper, matrixCount):
    distanceInfo1 = Point2Point(line1.startpoint, line1.endpoint, False)
    distanceInfo2 = Point2Point(line2.startpoint, line2.endpoint, False)

    sortedArr = sorted([(line1.startpoint[0], line1.startpoint[1],line1.startpoint[2]), (line2.startpoint[0], line2.startpoint[1],line1.startpoint[2])])
    if sortedArr[0] == line1.startpoint:
        distance, m_projectionpoint, m_coefficient = distancePoint2LineSegment(line1.startpoint, line1.endpoint,
                                                                               line2.startpoint, False)
        parallelDis = Point2Point(line1.startpoint, m_projectionpoint, False)
        if parallelDis +20> distanceInfo2:
            return False
    else:
        distance, m_projectionpoint, m_coefficient = distancePoint2LineSegment(line2.startpoint, line2.endpoint,
                                                                               line1.startpoint, False)
        parallelDis = Point2Point(line2.startpoint, m_projectionpoint, False)
        if parallelDis + 20 > distanceInfo1:
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

    if perpendicularDistance > -1:
        matrixper[line1.vIndex][line2.vIndex] += perDistance1[0] + perDistance2[0]
        matrixCount[line1.vIndex][line2.vIndex] += 1
        return True
    return False

def symmetrize(a):
    """
    Return a symmetrized version of NumPy array a.

    Values 0 are replaced by the array value at the symmetric
    position (with respect to the diagonal), i.e. if a_ij = 0,
    then the returned array a' is such that a'_ij = a_ji.

    Diagonal values are left untouched.

    a -- square NumPy array, such that a_ij = 0 or a_ji = 0,
    for i != j.
    """
    return a + a.T - numpy.diag(a.diagonal())

def computeScore(set, matrix):
    line1 = set[0]
    #line1  = LineSegment((1000000,1000000, 0), (15000000,15000000, 0), 0, 0, 0)
    currentIndex = 1
    #ang1 = angleLineSegment2LineSegment1((0, 1, 0), (1, 1, 0), line1.startpoint, line1.endpoint)

    while currentIndex < len(set):
        line2 = set[currentIndex]
        #line2 = LineSegment((2000000, 5000000, 0), (10000000, 19000000, 0), 0, 0, 0)
        currentIndex = currentIndex + 1

        arr = [(line1.startpoint), (line1.endpoint), (line2.startpoint), (line2.endpoint)]
        rArr = []
        sPoint = ((arr[0][0] + arr[2][0]) / 2, (arr[0][1] + arr[2][1]) / 2, (arr[0][2] + arr[2][2]) / 2)
        ePoint = ((arr[1][0] + arr[3][0]) / 2, (arr[1][1] + arr[3][1]) / 2, (arr[1][2] + arr[3][2]) / 2)
        AVdirVec = LineSegment(sPoint, ePoint, 0, 0, 0)
        ang = math.degrees(angleLineSegment2LineSegment((0, 1, 0), (1, 1, 0), AVdirVec.startpoint, AVdirVec.endpoint))
        for p in arr:
            newp = rotate(p, ang)
            rArr.append(newp)
        sortedArr = sorted(rArr)


        d1, m_projectionpoint1, m_coefficient1 = distancePoint2LineSegment(sPoint, ePoint, (sortedArr[1]))
        d2, m_projectionpoint2, m_coefficient2 = distancePoint2LineSegment(sPoint, ePoint, (sortedArr[2]))


        #d = Point2Point(m_projectionpoint1, m_projectionpoint2)
        d = Point2Point((sortedArr[1][0],0,0), (sortedArr[2][0],0,0))
        d1 = Point2Point((line1.startpoint), (line1.endpoint))
        d2 = Point2Point((line2.startpoint), (line2.endpoint))
        d11 = Point2Point((rArr[0]), (rArr[1]))
        d22 = Point2Point((rArr[2]), (rArr[3]))
        p = pp()
        p.plotLine([(line1.startpoint), (line1.endpoint)])
        p.plotLine([(line2.startpoint), (line2.endpoint)])
        p.plotLine([sPoint, ePoint])
        #p.plotLine([rArr[0], rArr[1]])
        #p.plotLine([rArr[2], rArr[3]])
        #p.plotLine([(sortedArr[1][0],0,0), (sortedArr[2][0],0,0)])
        #p.plotLine([m_projectionpoint1, m_projectionpoint2])
        p.Show()
        p = pp()
        p.plotLine([rArr[0], rArr[1]])
        p.plotLine([rArr[2], rArr[3]])
        p.plotLine([(sortedArr[1][0],0,0), (sortedArr[2][0],0,0)])
        #p.plotLine([m_projectionpoint1, m_projectionpoint2])
        #p.plotLine([sPoint, ePoint])
        #p.plotLine([m_projectionpoint1, sortedArr[1]])
        #p.plotLine([sortedArr[2], m_projectionpoint2])
        p.Show()
        matrix[line1.vIndex][line2.vIndex] += d
        matrix[line2.vIndex][line1.vIndex] += d
def computeScore2(set, matrix, matrixprozent):
    line1 = set[0]
    currentIndex = 1

    while currentIndex < len(set):
        line2 = set[currentIndex]
        currentIndex = currentIndex + 1

        arr = [(line1.startpoint), (line1.endpoint), (line2.startpoint), (line2.endpoint)]
        rArr = []
        sPoint = ((arr[0][0] + arr[2][0]) / 2, (arr[0][1] + arr[2][1]) / 2, (arr[0][2] + arr[2][2]) / 2)
        ePoint = ((arr[1][0] + arr[3][0]) / 2, (arr[1][1] + arr[3][1]) / 2, (arr[1][2] + arr[3][2]) / 2)
        AVdirVec = LineSegment(sPoint, ePoint, 0, 0, 0)
        ang = math.degrees(angleLineSegment2LineSegment((0, 1, 0), (1, 1, 0), AVdirVec.startpoint, AVdirVec.endpoint))
        d1, m_projectionpoint1, m_coefficient1 = distancePoint2LineSegment(sPoint, ePoint, line1.startpoint)
        d2, m_projectionpoint2, m_coefficient2 = distancePoint2LineSegment(sPoint, ePoint, (line1.endpoint))
        d3, m_projectionpoint3, m_coefficient3 = distancePoint2LineSegment(sPoint, ePoint, (line2.startpoint))
        d4, m_projectionpoint4, m_coefficient4 = distancePoint2LineSegment(sPoint, ePoint, line2.endpoint)
        arr = [m_projectionpoint1, m_projectionpoint2, m_projectionpoint3, m_projectionpoint4]
        for p in arr:
            newp = rotate(p, ang)
            rArr.append(newp)
        sortedArr = sorted(rArr)

        newp11 = rotate(sortedArr[1], -1*ang)
        newp12 = rotate(sortedArr[2], -1*ang)
        #p = pp()
        #p.plotLine([(line1.startpoint), (line1.endpoint)])
        #p.plotLine([(line2.startpoint), (line2.endpoint)])
        #p.plotLine([m_projectionpoint2, (line1.endpoint)])
        #p.plotLine([m_projectionpoint4, (line2.endpoint)])
        #p.plotLine([(line1.startpoint), m_projectionpoint1])
        #p.plotLine([(line2.startpoint), m_projectionpoint3])
        #p.plotLine([sPoint, ePoint])
        #p.Show()



        #d = Point2Point(m_projectionpoint1, m_projectionpoint2)
        d = Point2Point(newp11, newp12)
        #d1 = Point2Point((line1.startpoint), (line1.endpoint))
        #d2 = Point2Point((line2.startpoint), (line2.endpoint))

        d11 = Point2Point((line1.startpoint), (line1.endpoint))
        d22 = Point2Point((line2.startpoint), (line2.endpoint))
        d3 = (d11 + d22) / 2

        matrix[line1.vIndex][line2.vIndex] += d
        matrix[line2.vIndex][line1.vIndex] += d

        matrixprozent[line1.vIndex][line2.vIndex] += d3
        matrixprozent[line2.vIndex][line1.vIndex] += d3

def computeScore1(set, matrix, matrixprozent):
    line1 = set[0]

    currentIndex = 1


    while currentIndex < len(set):
        line2 = set[currentIndex]

        currentIndex = currentIndex + 1

        arr = [(line1.startpoint), (line1.endpoint), (line2.startpoint), (line2.endpoint)]
        rArr = []
        sPoint = ((arr[0][0] + arr[2][0]) / 2, (arr[0][1] + arr[2][1]) / 2, (arr[0][2] + arr[2][2]) / 2)
        ePoint = ((arr[1][0] + arr[3][0]) / 2, (arr[1][1] + arr[3][1]) / 2, (arr[1][2] + arr[3][2]) / 2)
        AVdirVec = LineSegment(sPoint, ePoint, 0, 0, 0)
        ang = math.degrees(
            angleLineSegment2LineSegment((0, 1, 0), (1, 1, 0), AVdirVec.startpoint, AVdirVec.endpoint))

        newpXaxis = rotate((0, 1, 0), ang)
        newp1Xaxis = rotate((1, 1, 0), ang)

        xOder = []
        for p in arr:
            d, m_projectionpoint, m_coefficient = distancePoint2LineSegment(newpXaxis, newp1Xaxis, p)
            xx1 = (p, m_projectionpoint[0],  m_projectionpoint)
            xOder.append(xx1)

        xOder.sort(key=operator.itemgetter(1))

        d1, m_projectionpoint1, m_coefficient1 = distancePoint2LineSegment(sPoint, ePoint, (xOder[1][0]))
        d2, m_projectionpoint2, m_coefficient2 = distancePoint2LineSegment(sPoint, ePoint, (xOder[2][0]))

        d = Point2Point(m_projectionpoint1,m_projectionpoint2)
        d11 = Point2Point((line1.startpoint), (line1.endpoint))
        d22 = Point2Point((line2.startpoint), (line2.endpoint))
        d3 = (d11 + d22) / 2
        ang1 = math.degrees(
            angleLineSegment2LineSegment((xOder[2][0]), m_projectionpoint2, AVdirVec.startpoint, AVdirVec.endpoint))

        #p = pp()

        #p.plotLine([(line1.startpoint), (line1.endpoint)])
        #p.plotLine([(line2.startpoint), (line2.endpoint)])
        #p.plotLine([m_projectionpoint1,m_projectionpoint2])
        #p.plotLine([m_projectionpoint1, (xOder[1][0])])
        #p.plotLine([(xOder[2][0]), m_projectionpoint2])
        #p.plotLine([(xOder[2][2]), xOder[1][2]])
        #p.Show()

        matrix[line1.vIndex][line2.vIndex] += d
        matrix[line2.vIndex][line1.vIndex] += d

        matrixprozent[line1.vIndex][line2.vIndex] += d3
        matrixprozent[line2.vIndex][line1.vIndex] += d3


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
    x = (math.cos(angle) * point[0]) - (math.sin(angle) * point[1])
    y = (math.sin(angle) * point[0]) + (math.cos(angle) * point[1])
    z = zc
    newpoint = (x, y, z)
    return newpoint
