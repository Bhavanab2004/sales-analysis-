import pandas as pd
import matplotlib.pyplot as plt
from collections import Counter
from itertools import combinations
df = pd.read_csv("C://project//all_data.csv")
print(df)
df.dropna(how='all', inplace=True)
df = df[df['Order Date'].str[0:2] != 'Or'] 
df['Quantity Ordered'] = pd.to_numeric(df['Quantity Ordered'], errors='coerce')
df['Price Each'] = pd.to_numeric(df['Price Each'], errors='coerce')
df['Order Date'] = pd.to_datetime(df['Order Date'], format='%m/%d/%y %H:%M')
df.dropna(inplace=True)
df['Month'] = df['Order Date'].dt.month
df['Hour'] = df['Order Date'].dt.hour
df['Sales'] = df['Quantity Ordered'] * df['Price Each']
df['City'] = df['Purchase Address'].apply(lambda x: x.split(',')[1].strip())
rows, columns = df.shape
print("Rows:", rows)
print("Columns:", columns)
monthly_sales = df.groupby('Month')['Sales'].sum()
city_orders = df['City'].value_counts()
hourly_orders = df.groupby('Hour')['Quantity Ordered'].count()
plt.figure(figsize=(10,5))
plt.bar(monthly_sales.index, monthly_sales.values)
plt.title("Monthly Sales")
plt.xlabel("Month")
plt.ylabel("Sales in USD")
plt.xticks(monthly_sales.index)
plt.grid(True)
plt.tight_layout()
plt.show()

plt.figure(figsize=(12,6))
plt.bar(city_orders.index, city_orders.values)
plt.title("Number of Orders by City")
plt.xlabel("City")
plt.ylabel("Orders")
plt.xticks(rotation='vertical')
plt.grid(True)
plt.tight_layout()
plt.show()

plt.figure(figsize=(10,5))
plt.plot(hourly_orders.index, hourly_orders.values, marker='o')
plt.title("Order Count by Hour")
plt.xlabel("Hour of Day")
plt.ylabel("Number of Orders")
plt.grid(True)
plt.xticks(range(0,24))
plt.tight_layout()
plt.show()
top_products = df.groupby('Product')['Quantity Ordered'].sum().sort_values(ascending=False)
plt.figure(figsize=(12,5))
plt.bar(top_products.index[:10], top_products.values[:10])
plt.xticks(rotation='vertical')
plt.title("Top 10 Best-Selling Products")
plt.xlabel("Product")
plt.ylabel("Quantity Sold")
plt.tight_layout()
plt.show()

df_dupes = df[df.duplicated(subset=['Order ID'], keep=False)]
df_dupes['Grouped'] = df_dupes.groupby('Order ID')['Product'].transform(lambda x: ','.join(x))
grouped = df_dupes[['Order ID', 'Grouped']].drop_duplicates()

count = Counter()
for row in grouped['Grouped']:
    items = row.split(',')
    count.update(Counter(combinations(items, 2)))
print("Top 10 Frequently Bought Together:")
for key, value in count.most_common(10):
    print(f"{key}: {value}")
monthly_trend = df.groupby(df['Order Date'].dt.to_period("M"))['Sales'].sum()
monthly_trend.index = monthly_trend.index.to_timestamp()
plt.figure(figsize=(10,5))
plt.plot(monthly_trend.index, monthly_trend.values, label="Monthly Sales")
plt.plot(monthly_trend.index, monthly_trend.rolling(3).mean(), label="3-Month MA", linestyle='--')
plt.title("Monthly Sales with Moving Average")
plt.xlabel("Month")
plt.ylabel("Sales")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()
