import pandas as pd

# Load our dataset
df = pd.read_csv("data/expenses.csv")

# Convert Date column to datetime
df["Date"] = pd.to_datetime(df["Date"])

print("========== DATASET OVERVIEW ==========")

print("\nNumber of rows:", len(df))
print("Number of columns:", len(df.columns))

print("\nColumn names:")
print(df.columns.tolist())

print("\n========== FIRST 5 RECORDS ==========")
print(df.head())

print("\n========== DATA TYPES ==========")
print(df.dtypes)

print("\n========== MISSING VALUES ==========")
print(df.isnull().sum())

print("\n========== DUPLICATE RECORDS ==========")
print(df.duplicated().sum())

print("\n========== TOTAL EXPENSE ==========")
print("₹", df["Amount"].sum())

print("\n========== AVERAGE EXPENSE ==========")
print("₹", round(df["Amount"].mean(), 2))

print("\n========== HIGHEST EXPENSE ==========")
print("₹", df["Amount"].max())

print("\n========== LOWEST EXPENSE ==========")
print("₹", df["Amount"].min())

print("\n========== EXPENSE BY CATEGORY ==========")
category_expense = df.groupby("Category")["Amount"].sum().sort_values(ascending=False)
print(category_expense)

print("\n========== EXPENSE BY PAYMENT METHOD ==========")
payment_expense = df.groupby("Payment_Method")["Amount"].sum().sort_values(ascending=False)
print(payment_expense)s