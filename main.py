import pandas as pd
import matplotlib.pyplot as plt
import os
from itertools import combinations 
from collections import Counter

def get_city (address):         # Function to get the city name
  return address.split(",")[1]

def get_state(address):         # Function to get the city state
  return address.split(",")[2].split(" ")[1]

# Merge the 12 months of sales data into a single CSV file
df = pd.read_csv("./Sales_Data/Sales_April_2019.csv")
files = [file for file in os.listdir("./Sales_Data")]
all_months_data = pd.DataFrame()
for file in files:
    df = pd.read_csv("./Sales_Data/" + file)
    all_months_data = pd.concat([all_months_data, df])
all_months_data.to_csv("all_data.csv", index=False)
all_data = pd.read_csv("all_data.csv")

# Clean up the data
nan_df = all_data[all_data.isna().any(axis=1)]
all_data = all_data.dropna(how="all") # Drop rows of NAN

all_data = all_data[all_data["Order Date"].str[0:2] != "Or"] # Find "Or" and delete it
all_data.head()

# Convert columns to the correct type
all_data["Quantity Ordered"] = pd.to_numeric(all_data["Quantity Ordered"])
all_data["Price Each"] = pd.to_numeric(all_data["Price Each"])

# Add a month column
all_data["Month"] = all_data["Order Date"].str[0:2]
all_data["Month"] = all_data["Month"].astype("int32")

# Add a sales column
all_data["Sales"] = all_data["Quantity Ordered"] * all_data["Price Each"]

# Add a city column
all_data["City"] = all_data["Purchase Address"].apply(lambda x:f"{get_city(x)} ({get_state(x)})") 
all_data

# Question 1: What was the best month for sales? How much was enrned that month?
results = all_data.groupby("Month").sum()
months = range(1, 13)
plt.bar(months, results["Sales"])
plt.xticks(months)
plt.xlabel("Month number")
plt.ylabel("Sales in USD ($)")
plt.show()

# Question 2: What city had the highest number of sales?
results = all_data.groupby("City").sum()
cities = [city for city, df in all_data.groupby("City")]
plt.bar(cities, results["Sales"])
plt.xticks(cities, rotation="vertical", size=8)
plt.xlabel("City name")
plt.ylabel("Sales in USD ($)")
plt.show()

# Question 3: What time should we display adverstiments to maximize likelihood 
# customer's buying product?
all_data["Order Date"] = pd.to_datetime(all_data["Order Date"])
all_data["Hour"] = all_data["Order Date"].dt.hour
all_data["Minute"] = all_data["Order Date"].dt.minute
all_data["Count"] = 1
hours = [hour for hour, df in all_data.groupby("Hour")]
plt.plot(hours, all_data.groupby(["Hour"]).count())
plt.xticks(hours)
plt.xlabel("Hour")
plt.ylabel("Number of Orders")
plt.grid()
plt.show()

# Question 4: What products are most often sold together?
df = all_data[all_data["Order ID"].duplicated(keep=False)]
df["Grouped"] = df.groupby("Order ID")["Product"].transform(lambda x: ",".join(x))
df = df[["Order ID", "Grouped"]].drop_duplicates()
count = Counter()
for row in df["Grouped"]:
    row_list = row.split(",")
    count.update(Counter(combinations(row_list , 2)))
for key, value in count.most_common(10):
    print(key, value)

# Question 5: What product sold the most? Why do you think it sold the most?
all_data.head()
product_group = all_data.groupby("Product")
quantity_ordered = product_group.sum()["Quantity Ordered"]
products = [product for product, df in product_group]
plt.bar(products, quantity_ordered)
plt.ylabel("Quantity Ordered")
plt.xlabel("Product")
plt.xticks(products, rotation="vertical", size=8)
plt.show()

prices = all_data.groupby("Product").mean()["Price Each"]
fig, ax1 = plt.subplots()
ax2 = ax1.twinx()
ax1.bar(products, quantity_ordered, color="g")
ax2.plot(products, prices, "b-")
ax1.set_xlabel("Product Name")
ax1.set_ylabel("Quantity Ordered", color = "g")
ax2.set_ylabel("Price ($)", color = "b")
ax1.set_xticklabels(products, rotation = "vertical", size=8)
plt.show()

