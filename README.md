# EcoRoute — Climate-Aware Route Planner

EcoRoute is a climate-aware routing web application that compares
shortest vs eco-optimal routes using offline OpenStreetMap data, live
air quality (AQI) and temperature, and displays them on a Leaflet map.

---

## 🧠 Features

✔ Offline routing using OSMnx + NetworkX  
✔ Shortest vs Eco route comparison (blue vs green)  
✔ Current location detection  
✔ Route distance and eco score calculation  
✔ Offline place search from Jaipur graph  
✔ Simple web UI using Leaflet

---

## 📁 Project Structure
EcoRoute-Climate-Aware-Route-Planner/
├── Backend/
│ ├── app.py
│ ├── routing.py
│ ├── search.py
│ ├── eco_cost.py
│ ├── jaipur_drive.graphml (not committed due to size)
│ └── requirements.txt
├── Frontend/
│ ├── index.html
│ ├── route.html
│ ├── main.css
│ ├── shared.css
│ ├── script.js
│ └── route.js
├── .gitignore
└── README.md

---

## 📦 Backend Setup

### Install dependencies

~~~bash
cd Backend
pip install -r requirements.txt
python app.py
~~~
## Frontend
Open Frontend/index.html in a browser
(or use Live Server in VS Code).

##Screenshots
Home Page
Route Comparison

## Note
The offline road network graph (jaipur_drive.graphml) is not included in the repository
due to file size constraints.
Routing currently works on an offline graph extracted for Jaipur city.
