import osmnx as ox
from math import sqrt

print("📂 Loading Jaipur graph for search...")
G = ox.load_graphml("jaipur_drive.graphml")


def haversine(lat1, lon1, lat2, lon2):
    return sqrt((lat1-lat2)**2 + (lon1-lon2)**2)


PLACE_NAMES = set()
NAME_TO_COORDS = {}

# ---------- NODE NAMES ----------
for _, data in G.nodes(data=True):
    name = data.get("name")
    if isinstance(name, str):
        PLACE_NAMES.add(name)
        NAME_TO_COORDS[name] = (data["y"], data["x"])  # lat, lon

# ---------- EDGE (ROAD) NAMES ----------
for u, v, data in G.edges(data=True):
    name = data.get("name")
    if isinstance(name, str):
        PLACE_NAMES.add(name)

        # midpoint of the road
        lat = (G.nodes[u]["y"] + G.nodes[v]["y"]) / 2
        lon = (G.nodes[u]["x"] + G.nodes[v]["x"]) / 2
        NAME_TO_COORDS.setdefault(name, (lat, lon))

    elif isinstance(name, list):
        for n in name:
            PLACE_NAMES.add(n)
            lat = (G.nodes[u]["y"] + G.nodes[v]["y"]) / 2
            lon = (G.nodes[u]["x"] + G.nodes[v]["x"]) / 2
            NAME_TO_COORDS.setdefault(n, (lat, lon))

PLACE_NAMES = sorted(PLACE_NAMES)

print(f"✅ Loaded {len(PLACE_NAMES)} searchable places")


def search_places(query, user_lat=None, user_lon=None, limit=10):
    q = query.lower()
    matches = []

    for name in PLACE_NAMES:
        if q in name.lower():
            coords = NAME_TO_COORDS.get(name)
            if coords and user_lat is not None:
                d = haversine(user_lat, user_lon, coords[0], coords[1])
            else:
                d = 9999
            matches.append((d, name))

    matches.sort(key=lambda x: x[0])
    return [name for _, name in matches[:limit]]



def get_place_coords(name):
    return NAME_TO_COORDS.get(name)
