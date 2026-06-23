import pandas as pd
import matplotlib

matplotlib.use('Agg')

import matplotlib.pyplot as plt
import seaborn as sns

#Load all Tables
data = pd.read_csv(r"D:\Data Engineer\Console data\Supply Chain Analysis\Supply_chain_dataset.csv")

#KPI Summary
total_sales = data['sales'].sum()
total_profit = data['profit_per_order'].sum()
total_orders = data['order_id'].nunique()
total_customers = data['customer_id'].nunique()

#print(f"Sales : {total_sales:,.0f}")
#print(f"Profit : {total_profit:,.0f}")
#print(f"Orders : {total_orders}")
#print(f"Customers : {total_customers}")

#Sales Analysis
plt.figure(figsize=(10,5))
sns.histplot(data['sales'], bins=50)
plt.title("Sales Distribution")
#plt.show

#Monthly Sales Trend
data['order_date'] = pd.to_datetime(data['order_date'])
monthly_sales = (data.groupby(pd.Grouper(key='order_date',freq='ME'))['sales'].sum())

monthly_sales.plot(figsize=(12,6))
plt.title("Monthly Sales Trend")
#plt.show()

#Profit Analysis
monthly_profit = (data.groupby(pd.Grouper(key='order_date',freq='ME'))['profit_per_order'].sum())

monthly_profit.plot(figsize=(12,6))
plt.title("Monthly Profit Trend")
#plt.show()

#Category Analysis
#category_sales = (data.groupby('category_name')['sales'].sum().sort_values(ascending=False))

#category_sales.plot(kind='bar',figsize=(12,6))
#plt.title("Sales by Category")
#plt.show()

#Product Analysis
#top_products = (data.groupby('product_name')['sales'].sum().sort_values(ascending=False).head(10))

#top_products.plot(kind='barh',figsize=(10,6))
#plt.title("Top Products by Sales")
#plt.show()

#Market Analysis
#market_sales = (data.groupby('market')['sales'].sum().sort_values(ascending=False))

#Shipping Analysis
#sns.boxplot(x=data['delivery_days'])

#Delay Analysis
data['label'].value_counts()
plt.close('all')
sns.countplot(x='label',data=data)
plt.title("Delivery Status")

#plt.show()

#Delay by Shipping Mode
pd.crosstab(data['shipping_mode'],data['label'])
#sns.heatmap(pd.crosstab(data['shipping_mode'],data['label']),annot=True,fmt='d')

#Profitability Analysis
data['profit_margin'] = (data['profit_per_order'] /data['sales'])
#print(data['profit_margin'].describe())

#sns.histplot(data['profit_margin'])

#Correlation Analysis
num_cols = [
    'sales',
    'profit_per_order',
    'product_price',
    'order_item_quantity',
    'delivery_days']
corr = data[num_cols].corr()

plt.figure(figsize=(8,6))
sns.heatmap(corr,annot=True,cmap='coolwarm')
plt.title("Correlation Matrix")
#plt.show()


