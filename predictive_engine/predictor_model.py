import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
import joblib

# 1. Load synthetic data
df = pd.read_csv("synthetic_ecoroute_data.csv")

# 2. Create future target (15 min = 3 steps ahead for 5-min intervals)
df["eco_cost_future"] = df["eco_cost"].shift(-3)

# Drop last rows with NaN target
df = df.dropna()

# 3. Features and target
X = df[[
    "traffic_density",
    "aqi",
    "temperature",
    "rain"
]]

y = df["eco_cost_future"]

# 4. Train-test split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# 5. Train model
model = LinearRegression()
model.fit(X_train, y_train)

# 6. Save model
joblib.dump(model, "eco_cost_predictor.pkl")

print("Predictive model trained and saved successfully!")
