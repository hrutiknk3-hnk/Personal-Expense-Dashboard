import pandas as pd
import random
from datetime import datetime, timedelta

# -----------------------------
# Project: Personal Expense Dashboard
# Purpose: Generate our own synthetic expense dataset
# -----------------------------

random.seed(42)

categories = {
    "Food": ["Breakfast", "Lunch", "Dinner", "Snacks"],
    "Transport": ["Bus", "Auto", "Cab", "Fuel"],
    "Education": ["Books", "Stationery", "Course", "Printing"],
    "Shopping": ["Clothes", "Accessories", "Personal Care"],
    "Entertainment": ["Movies", "Gaming", "Events"],
    "Bills": ["Mobile Recharge", "Internet", "Electricity"],
    "Health": ["Medicine", "Doctor", "Fitness"],
    "Other": ["Gift", "Miscellaneous", "Emergency"]
}

payment_methods = ["UPI", "Cash", "Card"]
necessity_values = ["Yes", "No"]
locations = ["College", "Home", "Mall", "Online", "Market", "City"]
moods = ["Happy", "Normal", "Stressed", "Excited"]

descriptions = {
    "Food": ["College meal", "Restaurant meal", "Snacks", "Coffee"],
    "Transport": ["Daily travel", "Bus journey", "Auto ride", "Cab ride"],
    "Education": ["Study material", "Notebook", "Course material", "Printing"],
    "Shopping": ["Clothing", "Accessories", "Personal item"],
    "Entertainment": ["Movie", "Game", "Event"],
    "Bills": ["Mobile recharge", "Internet bill", "Utility payment"],
    "Health": ["Medicine", "Health expense", "Fitness expense"],
    "Other": ["Gift", "Miscellaneous expense", "Unexpected expense"]
}

# Start date
start_date = datetime(2026, 4, 1)

records = []

# Generate 500 expense records
for i in range(500):

    date = start_date + timedelta(days=random.randint(0, 180))

    category = random.choice(list(categories.keys()))
    subcategory = random.choice(categories[category])

    description = random.choice(descriptions[category])

    # Generate realistic amount according to category
    if category == "Food":
        amount = random.randint(40, 400)
    elif category == "Transport":
        amount = random.randint(20, 500)
    elif category == "Education":
        amount = random.randint(50, 1500)
    elif category == "Shopping":
        amount = random.randint(200, 3000)
    elif category == "Entertainment":
        amount = random.randint(100, 1200)
    elif category == "Bills":
        amount = random.randint(100, 1500)
    elif category == "Health":
        amount = random.randint(100, 2000)
    else:
        amount = random.randint(50, 2000)

    payment_method = random.choice(payment_methods)
    necessity = random.choice(necessity_values)
    location = random.choice(locations)
    mood = random.choice(moods)

    records.append([
        date.strftime("%Y-%m-%d"),
        category,
        subcategory,
        description,
        amount,
        payment_method,
        necessity,
        location,
        mood
    ])

# Create DataFrame
df = pd.DataFrame(records, columns=[
    "Date",
    "Category",
    "Subcategory",
    "Description",
    "Amount",
    "Payment_Method",
    "Necessity",
    "Location",
    "Mood"
])

# Sort by date
df = df.sort_values("Date")

# Save dataset
df.to_csv("data/expenses.csv", index=False)

print("Dataset created successfully!")
print("Number of records:", len(df))
print("File saved to: data/expenses.csv")
print("\nFirst 5 records:")
print(df.head())