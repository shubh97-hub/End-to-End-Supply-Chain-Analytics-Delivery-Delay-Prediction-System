import pandas as pd
import numpy as np

#Load all Tables
data = pd.read_csv(r"D:\Data Engineer\Console data\Supply Chain Analysis\Supply_chain_dataset.csv")

# Data understanding
#print(data.shape)
#print(data.columns)
#print(data.info())
#print(data.describe())
#print(data.isnull().sum())
#print(data.duplicate().sum())
#print(data.dtypes)
#print(data['label'].value_counts())

data['order_date'] = pd.to_datetime(data['order_date'],utc=True)
data['shipping_date'] = pd.to_datetime(data['shipping_date'],utc=True)

#Creating Delivery Days
data['delivery_days'] = (data['shipping_date'] - data['order_date']).dt.days

data.to_csv(r"D:\Data Engineer\Console data\Supply Chain Analysis\Supply_chain_dataset.csv", index=False)
print(data.columns)