#SUPPLY CHAIN DELAY PREDICTION - XGBOOST VERSION
import pandas as pd
import numpy as np
import joblib
import warnings

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    classification_report)
from xgboost import XGBClassifier
warnings.filterwarnings("ignore")

#LOAD DATA
data = pd.read_csv(r"D:\Data Engineer\Console data\Supply Chain Analysis\Supply_chain_dataset.csv")

print(f"Dataset Shape: {data.shape}")

#DATE FEATURES

data["order_date"] = pd.to_datetime(data["order_date"],errors="coerce")

data["month"] = data["order_date"].dt.month
data["quarter"] = data["order_date"].dt.quarter
data["weekday"] = data["order_date"].dt.dayofweek

#FEATURE ENGINEERING

data["is_weekend"] = (data["weekday"] >= 5).astype(int)

data["profit_margin"] = (data["profit_per_order"] /(data["sales"] + 1))

data["discount_amount"] = (data["sales"] *data["order_item_discount_rate"])

#FEATURE LIST

features = [
    "sales",
    "order_item_quantity",
    "product_price",
    "profit_per_order",

    "shipping_mode",
    "market",
    "category_name",
    "department_name",
    "order_region",

    "delivery_days",

    "month",
    "quarter",
    "weekday",
    "is_weekend",

    "customer_country",
    "customer_state",

    "order_country",
    "order_state",
    "order_city",

    "payment_type",

    "order_item_discount",
    "order_item_discount_rate",

    "sales_per_customer",
    "order_item_profit_ratio",

    "profit_margin",
    "discount_amount"]

#ENCODE CATEGORICALS

categorical_cols = [
    "shipping_mode",
    "market",
    "category_name",
    "department_name",
    "order_region",

    "customer_country",
    "customer_state",

    "order_country",
    "order_state",
    "order_city",

    "payment_type"]

encoders = {}

for col in categorical_cols:

    le = LabelEncoder()

    data[col] = le.fit_transform(
        data[col].astype(str))
    encoders[col] = le

print("Encoding Complete")

#TARGET

target_map = {
    -1: 0,   # Early
     0: 1,   # On-Time
     1: 2    # Late
}

data["label"] = data["label"].map(target_map)

#PREPARE DATA

X = data[features]
y = data["label"]

#TRAIN TEST SPLIT

X_train, X_test, y_train, y_test = train_test_split(

    X,y,test_size=0.20,random_state=42,stratify=y)

print("Training Shape :", X_train.shape)
print("Testing Shape  :", X_test.shape)

#XGBOOST MODEL

model = XGBClassifier(
    objective="multi:softprob",
    num_class=3,
    n_estimators=800,
    learning_rate=0.03,
    max_depth=8,
    min_child_weight=3,
    subsample=0.8,
    colsample_bytree=0.8,
    gamma=0.1,
    random_state=42,
    eval_metric="mlogloss")

model.fit(X_train,y_train)

print("Training Complete")

#PREDICTIONS

y_pred = model.predict(X_test)

#EVALUATION

accuracy = accuracy_score(y_test,y_pred)

precision = precision_score(y_test,y_pred,average="weighted")

recall = recall_score(y_test,y_pred,average="weighted")

f1 = f1_score(y_test,y_pred,average="weighted")

print("MODEL PERFORMANCE")
print(f"Accuracy  : {accuracy:.4f}")
print(f"Precision : {precision:.4f}")
print(f"Recall    : {recall:.4f}")
print(f"F1 Score  : {f1:.4f}")

print("\nClassification Report")
print(classification_report(y_test,y_pred))

#FEATURE IMPORTANCE
importance = pd.DataFrame({"Feature": X.columns,
"Importance": model.feature_importances_})

importance = importance.sort_values(by="Importance",ascending=False)

print("Top 15 Features")

print(importance.head(15))

importance.to_csv("feature_importance.csv",index=False)


#SAVE FILES
joblib.dump(model,"delay_prediction_model.pkl")

joblib.dump(encoders,"label_encoders.pkl")

joblib.dump(features,"feature_columns.pkl")

print("Files Saved Successfully")
