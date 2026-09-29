import pandas as pd
import numpy as np

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from tensorflow.keras.callbacks import EarlyStopping



import joblib

# ---------------------------------------
# 1. Load Feature Dataset
# ---------------------------------------

DATA_PATH = "results/candidate_features.csv"

df = pd.read_csv(DATA_PATH)

print("Feature dataset loaded!")
print("Total Candidates:", len(df))


# ---------------------------------------
# 2. Create Pseudo Suitability Target
# ---------------------------------------

df["Suitability_Target"] = (
    df["Skill_Match"] * 0.40
    + df["JD_Similarity"] * 0.30
    + df["Experience_Score"] * 0.20
    + df["Education_Score"] * 0.10
)

print("\nPseudo suitability target created.")

print(
    df[
        [
            "Candidate_ID",
            "Skill_Match",
            "JD_Similarity",
            "Experience_Score",
            "Education_Score",
            "Suitability_Target"
        ]
    ].head()
)


# ---------------------------------------
# 3. Input Features
# ---------------------------------------

FEATURES = [
    "Skill_Match",
    "JD_Similarity",
    "Experience_Score",
    "Education_Score"
]

X = df[FEATURES]

y = df["Suitability_Target"]


# ---------------------------------------
# 4. Train/Test Split
# ---------------------------------------

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42
)

print("\nTraining Candidates:", len(X_train))
print("Testing Candidates:", len(X_test))


# ---------------------------------------
# 5. Feature Scaling
# ---------------------------------------

scaler = StandardScaler()

X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)


# ---------------------------------------
# 6. Neural Network
# ---------------------------------------

model = Sequential([
    Dense(
        16,
        activation="relu",
        input_shape=(X_train_scaled.shape[1],)
    ),

    Dense(
        8,
        activation="relu"
    ),

    Dense(
        1,
        activation="linear"
    )
])


model.compile(
    optimizer="adam",
    loss="mse",
    metrics=["mae"]
)


# ---------------------------------------
# 7. Train Model
# ---------------------------------------

early_stopping = EarlyStopping(
    monitor="val_loss",
    patience=20,
    restore_best_weights=True
)

print("\nTraining Neural Network...\n")

history = model.fit(
    X_train_scaled,
    y_train,
    validation_split=0.20,
    epochs=200,
    batch_size=16,
    callbacks=[early_stopping],
    verbose=0
)

print("Training completed!")
print("Epochs Used:", len(history.history["loss"]))


# ---------------------------------------
# 8. Test Predictions
# ---------------------------------------

predictions = model.predict(
    X_test_scaled,
    verbose=0
).flatten()


# ---------------------------------------
# 9. Evaluation
# ---------------------------------------

mae = mean_absolute_error(
    y_test,
    predictions
)

mse = mean_squared_error(
    y_test,
    predictions
)

rmse = np.sqrt(mse)

r2 = r2_score(
    y_test,
    predictions
)

print("\n============================")
print("MODEL EVALUATION")
print("============================")

print(f"MAE  : {mae:.4f}")
print(f"MSE  : {mse:.4f}")
print(f"RMSE : {rmse:.4f}")
print(f"R2   : {r2:.4f}")


# ---------------------------------------
# 10. Predict All Candidates
# ---------------------------------------

X_all_scaled = scaler.transform(
    df[FEATURES]
)

all_predictions = model.predict(
    X_all_scaled,
    verbose=0
).flatten()

# Keep score between 0 and 100
df["Neural_Network_Score"] = np.clip(
    all_predictions,
    0,
    100
)


# ---------------------------------------
# 11. Candidate Ranking
# ---------------------------------------

ranking_df = df.sort_values(
    by="Neural_Network_Score",
    ascending=False
).reset_index(drop=True)

ranking_df["Rank"] = ranking_df.index + 1


# ---------------------------------------
# 12. Save Results
# ---------------------------------------

ranking_df.to_csv(
    "results/neural_network_ranking.csv",
    index=False
)

joblib.dump(
    scaler,
    "models/scaler.pkl"
)
print("models/scaler.pkl")

print("\n============================")
print("TOP 10 NEUROHIRE CANDIDATES")
print("============================")

print(
    ranking_df[
        [
            "Candidate_ID",
            "Neural_Network_Score",
            "Rank"
        ]
    ].head(10)
)


print("\nSaved:")
print("results/neural_network_ranking.csv")
print("models/neurohire_model.keras")