import networkx as nx
from neo4j import GraphDatabase
from MercatorProjection import geodetic_to_ecef
from VehicleTrip import VehicleTrip


class Graph:

    def __init__(self):
        self.driver = GraphDatabase.driver("bolt://localhost:7687", auth=("neo4j", "samer"))
        self.Points = []
        self.VehicleTrips = []

    def close(self):
        self.driver.close()

    def getVehicleSetTrips(self):
        with self.driver.session() as session:
            result = session.run("MATCH (n:VehicleSet) where ID(n) = 2850 with n Limit 1 Match (n)-[r:CONSISTS_OF]->(rp:Vehicle) with rp"
                                  " MATCH (rp)-[:START_AT]->(n1:RoadPoint), (rp)-[:END_AT]->(n2:RoadPoint)"
                                  " CALL algo.shortestPath.stream(n1, n2, 'distance',{relationshipQuery:'ROAD_SEGMENT'})"
                                  " YIELD nodeId, cost"
                                  " RETURN algo.getNodeById(nodeId) as Node, ID(rp) as Id ")
            records = []
            for record in result:
                records.append(record)
            #pointsLine = []
            v = VehicleTrip()
            index = -1
            for rec in records:
                if v.id != rec[1] or rec == records[len(records) - 1]:
                    if v.id != None:
                        v.orgin = pointsLine[0]
                        v.end = pointsLine[len(pointsLine) - 1]
                        v.points = pointsLine
                        v.orginId = pointsID[0]
                        v.endId = pointsID[len(pointsID) - 1]
                        self.VehicleTrips.append(v)
                    v = VehicleTrip()
                    v.id = rec[1]
                    index = index + 1
                    v.index = index
                    pointsLine = []
                    pointsID = []
                lat = rec[0].get("lat")
                lon = rec[0].get("lon")
                pointId = rec[0].id
                r = None
                x, y, z = geodetic_to_ecef(lat, lon, 0)
                z = 0
                p1 = (x, y, z)
                pointsID.append(pointId)
                pointsLine.append(p1)

    def getVTripbyID(self, id):
        matches = next(x for x in self.VehicleTrips  if x.id == id)

        matches.drawLine(2)

    def get_data(self):
        # init graph
        graph = nx.DiGraph()
        # add nodes to graph
        graphDB_Session = self.driver.session()

        res = graphDB_Session.run("match (n:RoadPoint)  return n, ID(n) as id")


        results = [record for record in res.data()]
        for res in results:
            graph.add_node(res["id"], x=res['n'].get("x"), y=res['n'].get("y"), lat=res['n'].get("lat"), lon=res['n'].get("lon"))

        # add edges to graph
        res = graphDB_Session.run("match (n)-[r:ROAD_SEGMENT]-(m)  return ID(n) as nid ,ID(m) as mid ,r.distance as distance, r.distance_meter as dMeter, ID(r) as rid")
        results = [record for record in res.data()]
        for res in results:
            graph.add_edge(res["nid"], res["mid"], key=res["rid"], weight=res["distance"], attr_dict={'id': res["mid"]})

        # get vehicles
        res = graphDB_Session.run("MATCH (n:RoadPoint)-[:START_AT]-(v:Vehicle)-[:END_AT]-(m) RETURN n,v,m,ID(v) as vid, ID(n) as nid, ID(m) as mid")
        results = [record for record in res.data()]
        vehicles = {}
        vehicle_locations = {}
        for res in results:
            vehicles[res["vid"]] = (res["nid"] , res["mid"] )
            vehicle_locations[res["vid"]] = ((res["n"].get("lat"), res["n"].get("lon")), (res["m"].get("lat"), res["m"].get("lon")))

        return graph, vehicles, vehicle_locations