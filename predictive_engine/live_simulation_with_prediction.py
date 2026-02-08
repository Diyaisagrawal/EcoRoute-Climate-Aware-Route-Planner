import pandas as pd
import time
import joblib

# Load trained model
model = joblib.load("eco_cost_predictor.pkl")

# Load synthetic data
df = pd.read_csv("synthetic_ecoroute_data.csv")

THRESHOLD = 10  # eco-cost increase trigger

print("\n🚦 EcoRoute Live Predictive Simulation Started\n")

for _, row in df.iterrows():

    # Current live data
    current = {
        "traffic_density": row["traffic_density"],
        "aqi": row["aqi"],
        "temperature": row["temperature"],
        "rain": row["rain"],
        "eco_cost": row["eco_cost"]
    }

    # Predict future eco-cost
    input_df = pd.DataFrame([{
        "traffic_density": current["traffic_density"],
        "aqi": current["aqi"],
        "temperature": current["temperature"],
        "rain": current["rain"]
    }])

    predicted_eco_cost = model.predict(input_df)[0]

    # Decision logic
    print(f"⏱ Time: {row['timestamp']}")
    print(f"Current Eco-Cost   : {round(current['eco_cost'], 2)}")
    print(f"Predicted Eco-Cost : {round(predicted_eco_cost, 2)}")

    if predicted_eco_cost - current["eco_cost"] > THRESHOLD:
        print("🔄 REROUTE RECOMMENDED (eco-cost rising)")
    else:
        print("✅ Route Stable")

    print("-" * 50)

    time.sleep(3)

