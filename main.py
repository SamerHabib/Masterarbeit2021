import numpy

from Classifying import classifyTheLineSegments, computeScore
from Graph import *
from Optimization import *
from Partitioning import findoptimalpartition
from multiprocessing import Pool
import time

from Plotlib import *
from matrix import build

if __name__ == '__main__':
    start_time = time.time()
    print("---Start %s seconds ---" % (time.time() - start_time))
    g = Graph()
    g.getVehicleSetTrips()
    vehicleTrips = g.VehicleTrips
    print("---Init %s seconds ---" % (time.time() - start_time))
    start_time = time.time()
    pool = Pool()  # Create a multiprocessing Pool
    listV = pool.map(findoptimalpartition, vehicleTrips)
    pool.close()

    allLineSegments = []
    for x in listV:
        allLineSegments += x.getLineSegments()
    print("---Partition %s seconds ---" % (time.time() - start_time))
    start_time = time.time()
    allSet = classifyTheLineSegments(allLineSegments)
    print("---Classify %s seconds ---" % (time.time() - start_time))
    start_time = time.time()
    numberOfVehicles = len(vehicleTrips)
    matrix = numpy.zeros(shape=(numberOfVehicles, numberOfVehicles))

    for set in allSet:
        computeScore(set, matrix)

    MatrixNorm = matrix / numpy.abs(matrix).max()

    Groups = []
    Groups += build(vehicleTrips, MatrixNorm)
    print("---Groups %s seconds ---" % (time.time() - start_time))
    start_time = time.time()
    # use "definitions()" to create own network
    # road network import
    road_network, saving_factor, every_value = definitions()

    # use Neo4jConnection to use a neo4j database
    road_network, group, vehicle_locations = g.get_data()

    # run the model and return variables and model
    for g in Groups:
        print("----------------------------------------------------")
        model, x, y = optimization_model(road_network, g, saving_factor)
        # generate output
        #output_text(road_network, g, model, x, y, every_value)
    print("---Opt %s seconds ---" % (time.time() - start_time))



    i = 0





