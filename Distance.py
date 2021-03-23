import math

import numpy as np

from Vectors import *

# Function to find distance https://www.geeksforgeeks.org/program-to-calculate-distance-between-two-points-in-3-d/
def Point2Point(point1, point2, withoutZ = False):
    x1, y1, z1 = point1
    x2, y2, z2 = point2
    if(withoutZ):
        z1 = z2 = 0
    d = math.sqrt(math.pow(x2 - x1, 2) +
                  math.pow(y2 - y1, 2) +
                  math.pow(z2 - z1, 2) * 1.0)
    return d

def perpendicularDistanceLineSegment2LineSegment(fpoint, spoint, fpoint2, spoint2, withoutZ = False):
    distance1, m_projectionpoint1, m_coefficient1 = distancePoint2LineSegment(fpoint, spoint, fpoint2, withoutZ)
    distance2, m_projectionpoint2, m_coefficient2 = distancePoint2LineSegment(fpoint, spoint, spoint2, withoutZ)

    if distance2 == 0.0 and distance1 == 0.0:
        return 0.0
    return (math.pow(distance1, 2) + math.pow(distance2, 2)) / (distance2 + distance1)

def distancePoint2LineSegment(spoint, epoint, point,withoutZ = False):
    x, y, z = point
    sx, sy, sz = spoint
    ex, ey, ez = epoint

    if(withoutZ):
        sz = ez = z = 0
    vector1 = x - sx, y - sy, z - sz
    vector2 = ex - sx, ey - sy, ez - sz
    dd = np.cross([ex - sx, ey - sy], [sx - x, sy - y])
    # a coefficient(0 <= b <= 1)
    m_coefficient = computeDotProduct(vector1, vector2) / (
            computeDotProduct(vector2, vector2) + 0.000000000000000001)
    if math.isnan(m_coefficient):
        m_coefficient = 0.0
    m_projectionpoint = (
    sx + (vector2[0] * m_coefficient), sy + (vector2[1] * m_coefficient), sz * (vector2[2] * m_coefficient))
    if epoint == point:
        return (0, point, 0)
    # plt.plot((point.x, m_projectionpoint.x), (point.y, m_projectionpoint.y))
    distance = Point2Point(point, m_projectionpoint, True)
    dinfo = (distance, m_projectionpoint, m_coefficient)
    return dinfo

def angleLineSegment2LineSegment1(s1, e1, s2, e2):
    alpha1 = math.atan2(e1[1] - s1[1], e1[0] - s1[0])
    alpha2 = math.atan2(e2[1] - s2[1], e2[0] - s2[0])
    angle = math.fabs(np.degrees(alpha2 - alpha1))
    return angle

def angleDisntanceLineSegment2LineSegment(s1, e1, s2, e2):
    alpha1 = math.atan2(e1[1] - s1[1], e1[0] - s1[0])
    alpha2 = math.atan2(e2[1] - s2[1], e2[0] - s2[0])
    d1 = math.fabs(Point2Point(e1, s1, True))
    d2 = math.fabs(Point2Point(e2, s2, True))
    d = max(d1, d2)
    angd = d * math.fabs(math.sin(alpha2 - alpha1))
    return angd

def cosAngleLineSegment2LineSegment(s1, e1, s2, e2):
    v1 = vector(s1, e1)
    v2 = vector(s2, e2)
    cost = dotproduct(v1, v2) / (length1(v1) * length1(v2))
    return cost

def angleLineSegment2LineSegment(s1, e1, s2, e2):
    cost = cosAngleLineSegment2LineSegment(s1, e1, s2, e2)
    angle = math.acos(cost)
    return angle
