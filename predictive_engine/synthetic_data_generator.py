import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# 1. Time settings
start_time = datetime(2025, 1, 1, 0, 0)
intervals = 288  # 24 hours, 5-min interval
timestamps = [start_time + timedelta(minutes=5*i) for i in range(intervals)]

data = []

for t in timestamps:
    hour = t.hour

    # 2. Traffic pattern (peak hours)
    if 8 <= hour <= 10 or 18 <= hour <= 21:
        traffic = np.random.normal(80, 10)
    elif 0 <= hour <= 5:
        traffic = np.random.normal(20, 5)
    else:
        traffic = np.random.normal(50, 10)

    traffic = np.clip(traffic, 0, 100)

    # 3. Weather
    temperature = np.random.normal(30, 5)
    rain = np.random.choice([0, 0.3, 0.6], p=[0.7, 0.2, 0.1])

    # 4. AQI depends on traffic + weather
    aqi = 50 + (traffic * 1.5) + (rain * 20)
    aqi = np.clip(aqi, 50, 300)

    # 5. Eco-cost function
    eco_cost = (
        0.4 * traffic +
        0.4 * (aqi / 3) +
        0.1 * temperature +
        0.1 * (rain * 100)
    )

    data.append([t, traffic, aqi, temperature, rain, eco_cost])

# 6. Create DataFrame
df = pd.DataFrame(data, columns=[
    "timestamp",
    "traffic_density",
    "aqi",
    "temperature",
    "rain",
    "eco_cost"
])

# 7. Save
df.to_csv("synthetic_ecoroute_data.csv", index=False)
print("Synthetic data generated successfully!")
