# EcoRoute – Climate-Aware Route Planner

EcoRoute is a climate-aware route planning system that compares the shortest route with an eco-optimized route using air quality and temperature data.

## Features
- Offline routing using OpenStreetMap (OSMnx)
- Shortest vs Eco route comparison
- Eco Score based on AQI and temperature
- Current location support
- Offline place search (Jaipur)

## Tech Stack
- Python (Flask, OSMnx, NetworkX)
- JavaScript (Leaflet)
- OpenStreetMap
- OpenWeatherMap API

## How to Run

### Backend
```bash
cd Backend

pip install -r requirements.txt
python app.py

> Note: The offline road network graph is not included due to size constraints. It must be generated or downloaded separately.
