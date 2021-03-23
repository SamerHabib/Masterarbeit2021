import numpy as np
import math


def computeDotProduct(vector1, vector2):
    return np.dot(vector1, vector2)


def dot(v, w):
    x = v.x
    y = v.y
    X = w.x
    Y = w.y
    return x * X + y * Y


def length(v):
    return math.sqrt(computeDotProduct(v, v))

def vector(spoint, epoint):
    vector = (epoint[0] - spoint[0], epoint[1] - spoint[1])
    return vector


def unit(v):
    x = v.x
    y = v.y
    mag = length(v)
    return (x / mag, y / mag)


def distance(p0, p1):
    return length(vector(p0, p1))


def scale(v, sc):
    x = v.x
    y = v.y
    return (x * sc, y * sc)


def add(v, w):
    x = v.x
    y = v.y
    X = w.x
    Y = w.y
    return (x + X, y + Y)

def dotproduct(v1, v2):
  return sum((a*b) for a, b in zip(v1, v2))

def length1(v):
  return math.sqrt(dotproduct(v, v))
