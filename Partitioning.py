import math

from Distance import *

def findoptimalpartition(VehicleTrip):
    points = VehicleTrip.points
    start_index = 0
    length = 1
    start_point = points[0]

    VehicleTrip.partitionpoints.append(start_point)
    count = len(points)
    mdl_nonpar = 0
    mdl_par = 0
    while length + start_index < count:
        currIndex = start_index + length
        mdl_nonpar += compute_model_cost(points, start_index, currIndex)
        mdl_par = compute_model_cost(points, start_index, currIndex) + compute_encoding_cost(points, start_index, currIndex)
        if mdl_par > mdl_nonpar:
            VehicleTrip.partitionpoints.append(points[currIndex - 1])
            start_index = currIndex - 1
            length = 1
            mdl_nonpar = 0
            mdl_par = 0
        else:
            length += 1

    end_point = points[count - 1]
    VehicleTrip.partitionpoints.append(end_point)
    return VehicleTrip


def compute_model_cost(points, s_index, e_index):
    first_point = points[s_index]
    second_point = points[e_index]
    distance = Point2Point(first_point, second_point, True)
    if distance < 1.0:
        distance = 1.0
    return int(math.ceil(math.log2(distance)))


def compute_encoding_cost(points, s_index, e_index):
    clusterComponentStart = points[s_index]
    clusterComponentEnd = points[e_index]
    encodingCost = 0
    x = s_index
    while x < e_index:
        lineSegmentStart = points[x]
        lineSegmentEnd = points[x + 1]
        perpendicularDistance = perpendicularDistanceLineSegment2LineSegment(clusterComponentStart, clusterComponentEnd, lineSegmentStart, lineSegmentEnd, True)
        angleDistance = angleDisntanceLineSegment2LineSegment(clusterComponentStart, clusterComponentEnd, lineSegmentStart, lineSegmentEnd)
        if perpendicularDistance < 1.0: perpendicularDistance = 1.0  # to take logarithm
        if angleDistance < 1.0: angleDistance = 1.0
        encodingCost += int(math.ceil(math.log2(perpendicularDistance))) + int(math.ceil(math.log2(angleDistance)))
        x += 1
    return encodingCost