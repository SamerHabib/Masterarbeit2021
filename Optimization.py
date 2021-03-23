from gurobipy import *
import networkx as nx
from typing import Tuple, Dict

# define the graph and the vehicles
def definitions() -> Tuple[nx.DiGraph, float, bool]:

    # define here, if the output should show EVERY variable or just the ones, which are not equal to zero
    every_value = False

    # saving factor for model (standard is 0.1!)
    saving_factor = 0.1

    graph = nx.DiGraph()

    # define the network here:
    # every node needs an ID and it's coordinates: (node_ID, {"coords":[y_coordinate, x_coordinate]})
    # input is a list of nodes:
    graph.add_nodes_from([(1, {"coords": [1, 1]}), (2, {"coords": [1, 2]}), (3, {"coords": [2, 1]}), (4, {"coords": [2, 2]})])

    # define edges here, every edge needs the starting node and the ending node, also the weight!
    graph.add_edges_from([(1, 2, {'weight': 10}), (2, 3, {'weight': 90}), (1, 3, {'weight': 100}),
                          (1, 4, {'weight': 40}), (4, 3, {'weight': 40})])

    # define !2! vehicle here

    return graph, saving_factor, every_value


# the model to be optimized
def optimization_model(road_network, group, saving_factor=0.1):

    # model init
    model = Model("Routing")
    x = {}
    y = {}

    # initiate the variables with costs
    for edge in road_network.edges():

        x[edge] = {}
        y[edge] = model.addVar(vtype=GRB.BINARY, obj=saving_factor * road_network.get_edge_data(*edge)["weight"])

        for h in group:
            x[edge][h.id] = model.addVar(vtype=GRB.BINARY, lb=0, obj=(1 - saving_factor) * road_network.get_edge_data(*edge)["weight"])

    model.update()

    # flow condition
    for v in road_network.nodes():
        for h in group:
            if h.orginId == v:
                b = 1
            elif h.endId == v:
                b = -1
            else:
                b = 0
            model.addConstr(quicksum(x[edge][h.id] for edge in road_network.out_edges(v)) - quicksum(x[edge][h.id] for edge in road_network.in_edges(v)) == b, name='flow_' + str(v) + "_" + str(h))

    # buying of edge
    for edge in road_network.edges():
        for h in group:
            model.addConstr(x[edge][h.id] <= y[edge])

    # optimize the model
    model.optimize()

    return model, x, y


def output_text(road_network: nx.DiGraph, group: Dict, model, x: Dict, y: Dict, every_value=True) -> None:
    # print optimal solution:
    print("Optimal solution value: " + str(model.ObjVal))

    # generate output lines to show variables
    if every_value:
        for e in road_network.edges():
            print("edge " + str(e) + " has value: " + str(y[e].X))
            for h in group:
                print("vehicle " + str(h.id) + " on the edge " + str(e) + " has : " + str(x[e][h.id].X))
    else:
        for e in road_network.edges():
            if y[e].X > 0.99:
                print("edge " + str(e) + " has value: " + str(y[e].X))
                for h in group:
                    print("vehicle " + str(h.id) + " on the edge " + str(e) + " has : " + str(x[e][h.id].X))
