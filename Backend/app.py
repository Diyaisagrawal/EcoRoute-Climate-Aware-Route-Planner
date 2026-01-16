from flask import Flask, request, jsonify
from flask_cors import CORS

from routing import get_route
from search import search_places, get_place_coords

app = Flask(__name__)
CORS(app)

print("🔥 app.py loaded")


# ---------- ROUTE: ECO ROUTE ----------
@app.route("/eco-route", methods=["POST"])
def eco_route():
    data = request.json

    start = tuple(data["start"])   # [lat, lon]
    end = tuple(data["end"])
    aqi = data.get("aqi", 80)
    temp = data.get("temp", 30)

    geojson = get_route(start, end, aqi, temp)

    if geojson is None:
        return jsonify({"error": "No route found"}), 400

    return jsonify(geojson)


# ---------- ROUTE: OFFLINE SEARCH ----------
@app.route("/search")
def search():
    q = request.args.get("q", "")
    lat = request.args.get("lat", type=float)
    lon = request.args.get("lon", type=float)

    return jsonify(search_places(q, lat, lon))



# ---------- ROUTE: PLACE → COORDS ----------
@app.route("/place-coords", methods=["GET"])
def place_coords():
    name = request.args.get("name")
    coords = get_place_coords(name)

    if not coords:
        return jsonify({"error": "Not found"}), 404

    return jsonify({"lat": coords[0], "lon": coords[1]})


if __name__ == "__main__":
    app.run(debug=True)
