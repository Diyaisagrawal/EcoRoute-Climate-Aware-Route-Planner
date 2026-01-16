import osmnx as ox
import networkx as nx
from eco_cost import eco_penalty
from math import radians, sin, cos, sqrt, atan2

def haversine(lat1, lon1, lat2, lon2):
    R = 6371  # Earth radius in km
    dlat = radians(lat2 - lat1)
    dlon = radians(lon2 - lon1)

    a = sin(dlat / 2) ** 2 + cos(radians(lat1)) * cos(radians(lat2)) * sin(dlon / 2) ** 2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    return R * c


print("📂 Loading offline Jaipur graph...")
G = ox.load_graphml("jaipur_drive.graphml")
print("✅ Jaipur graph loaded")

ROAD_PENALTY = {
    "motorway": 2.0,
    "trunk": 1.8,
    "primary": 1.5,
    "secondary": 1.3,
    "tertiary": 1.2,
    "residential": 1.0,
    "service": 0.9
}



def to_feature(nodes, color):
    return {
        "type": "Feature",
        "geometry": {
            "type": "LineString",
            "coordinates": [
                [G.nodes[n]["x"], G.nodes[n]["y"]] for n in nodes
            ]
        },
        "properties": {
            "color": color
        }
    }


def route_length(nodes):
    total = 0
    for i in range(len(nodes) - 1):
        lat1 = G.nodes[nodes[i]]["y"]
        lon1 = G.nodes[nodes[i]]["x"]
        lat2 = G.nodes[nodes[i + 1]]["y"]
        lon2 = G.nodes[nodes[i + 1]]["x"]

        total += haversine(lat1, lon1, lat2, lon2)

    return total



def get_route(start, end, aqi, temp):
    try:
        penalty = eco_penalty(aqi, temp)

        # Add eco weight once per request
        for _, _, _, data in G.edges(keys=True, data=True):
            length = data.get("length", 1)
            highway = data.get("highway", "residential")
            if isinstance(highway, list):
                highway = highway[0]
            road_factor = ROAD_PENALTY.get(highway, 1.1)
            data["eco_weight"] = length * road_factor * penalty


        # Nearest nodes (IMPORTANT: lon, lat)
        start_node = ox.distance.nearest_nodes(G, start[1], start[0])
        end_node = ox.distance.nearest_nodes(G, end[1], end[0])

        # Shortest & Eco routes
        shortest_nodes = nx.shortest_path(
            G, start_node, end_node, weight="length"
        )

        eco_nodes = nx.shortest_path(
            G, start_node, end_node, weight="eco_weight"
        )

        # Distances
        shortest_km = route_length(shortest_nodes)
        eco_km = route_length(eco_nodes)

        eco_score = eco_km * (aqi / 50) * (temp / 30)


        return {
            "type": "FeatureCollection",
            "features": [
                to_feature(shortest_nodes, "blue"),
                to_feature(eco_nodes, "green")
            ],
            "summary": {
                "shortest_km": round(shortest_km, 2),
                "eco_km": round(eco_km, 2),
                "eco_score": round(eco_score, 2)
            }
        }

    except Exception as e:
        print("🔥 ROUTING ERROR:", e)
        return None
