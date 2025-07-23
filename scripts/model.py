import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.neural_network import MLPRegressor
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mean_squared_error
from joblib import dump
import numpy as np

# Load the dataset
df = pd.read_csv("simulated_investor_profiles.csv")

# Features
X = df[[ 
    "age", "income", "capital", "expenses", "emi", "liquidity_need",
    "dependents", "confidence", "knowledge", "comfort_with_negatives",
    "market_awareness", "experience"
]]

# Targets (weights) — row-normalize instead of softmax
Y_raw = df[[f"weight_{asset}" for asset in ['equity', 'debt', 'gold', 'real_estate', 'crypto', 'cash']]]
Y = Y_raw.div(Y_raw.sum(axis=1), axis=0)  # Ensure weights sum to 1

# Scale inputs
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Split data
X_train, X_test, y_train, y_test = train_test_split(X_scaled, Y, test_size=0.2, random_state=42)

# Define and train model
model = MLPRegressor(
    hidden_layer_sizes=(64, 32),
    activation='relu',
    solver='adam',
    max_iter=500,
    random_state=42
)
model.fit(X_train, y_train)

# Save model and scaler
dump(model, "trained_allocation_model.joblib")
dump(scaler, "scaler.joblib")

# Evaluate
preds = model.predict(X_test)
mse = mean_squared_error(y_test, preds)
print(f"Test MSE: {mse:.5f}")

# Predict on a new sample
sample = X_test[0].reshape(1, -1)
predicted_weights = model.predict(sample)[0]

# Clip to ensure no negatives and re-normalize
predicted_weights = np.clip(predicted_weights, 0, None)
normalized = predicted_weights / predicted_weights.sum()

# Display
print("\nPredicted asset allocation (normalized after prediction):")
for asset, weight in zip(['equity', 'debt', 'gold', 'real_estate', 'crypto', 'cash'], normalized):
    print(f"{asset}: {weight * 100:.2f}%")

# Debug
print(f"\nSum of weights: {normalized.sum():.5f}")
print(f"Any negative weights? {any(normalized < 0)}")
