#PREDICTION RESULTS CSV
import pandas as pd
import numpy as np
import joblib
import warnings
from sklearn.model_selection import train_test_split

warnings.filterwarnings("ignore")

#LOAD SAVED ARTIFACTS
model = joblib.load("delay_prediction_model.pkl")
encoders = joblib.load("label_encoders.pkl")
features = joblib.load("feature_columns.pkl")

print("Model, encoders, and feature list loaded")

#LOAD DATA
data = pd.read_csv(r"D:\Data Engineer\Console data\Supply Chain Analysis\Supply_chain_dataset.csv")

#DATE FEATURES
data["order_date"] = pd.to_datetime(data["order_date"], errors="coerce")
data["month"] = data["order_date"].dt.month
data["quarter"] = data["order_date"].dt.quarter
data["weekday"] = data["order_date"].dt.dayofweek

#FEATURE ENGINEERING
data["is_weekend"] = (data["weekday"] >= 5).astype(int)
data["profit_margin"] = (data["profit_per_order"] / (data["sales"] + 1))
data["discount_amount"] = (data["sales"] * data["order_item_discount_rate"])

#ENCODE CATEGORICALS (use SAVED encoders, not new ones)
categorical_cols = [
    "shipping_mode", "market", "category_name", "department_name", "order_region",
    "customer_country", "customer_state",
    "order_country", "order_state", "order_city",
    "payment_type"]

for col in categorical_cols:
    le = encoders[col]
    # handle unseen categories safely
    data[col] = data[col].astype(str).map(
        lambda x: x if x in le.classes_ else "UNKNOWN")
    if "UNKNOWN" not in le.classes_:
        le.classes_ = np.append(le.classes_, "UNKNOWN")
    data[col] = le.transform(data[col])

print("Encoding Complete")

#TARGET
target_map = {-1: 0, 0: 1, 1: 2}
data["label"] = data["label"].map(target_map)

#PREPARE DATA
X = data[features]
y = data["label"]

#SAME TRAIN/TEST SPLIT AS TRAINING (same random_state!)

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.20, random_state=42, stratify=y)

print("Test Shape:", X_test.shape)

#PREDICTIONS
y_pred = model.predict(X_test)
y_pred_proba = model.predict_proba(X_test)

#BUILD RESULTS
label_name_map = {0: "Early", 1: "On-Time", 2: "Late"}
results = data.loc[X_test.index].copy()

results["actual_label"] = y_test.values
results["predicted_label"] = y_pred

results["actual_status"] = results["actual_label"].map(label_name_map)
results["predicted_status"] = results["predicted_label"].map(label_name_map)

results["prob_early"] = y_pred_proba[:, 0]
results["prob_on_time"] = y_pred_proba[:, 1]
results["prob_late"] = y_pred_proba[:, 2]

results["prediction_confidence"] = y_pred_proba.max(axis=1)

results["correct_prediction"] = (results["actual_label"] == results["predicted_label"]).astype(int)

output_cols = ["order_date"] + features + [
    "actual_label", "predicted_label",
    "actual_status", "predicted_status",
    "prob_early", "prob_on_time", "prob_late",
    "prediction_confidence", "correct_prediction"]

output_cols = [c for c in output_cols if c in results.columns]

prediction_results = results[output_cols]
prediction_results.to_csv("prediction_results.csv", index=False)

print(f"prediction_results.csv saved with {prediction_results.shape[0]} rows and {prediction_results.shape[1]} columns")
print(prediction_results.head())

correct_count = prediction_results["correct_prediction"].sum()
total_count = len(prediction_results)
print(f"\nCorrect Predictions : {correct_count} / {total_count} ({correct_count/total_count:.2%})")