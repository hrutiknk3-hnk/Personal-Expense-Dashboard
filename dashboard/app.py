import streamlit as st
import pandas as pd
import plotly.express as px

# -----------------------------
# Page Configuration
# -----------------------------

st.set_page_config(
    page_title="Personal Expense Dashboard",
    page_icon="💰",
    layout="wide"
)
# -----------------------------
# Custom Dashboard Styling
# -----------------------------

st.markdown("""
<style>

.main {
    padding-top: 1rem;
}

h1 {
    font-size: 2.5rem !important;
    font-weight: 700 !important;
}

h2 {
    font-size: 1.8rem !important;
    margin-top: 2rem !important;
}

h3 {
    font-size: 1.4rem !important;
}

[data-testid="stMetric"] {
    background: linear-gradient(
        135deg,
        rgba(255, 255, 255, 0.08),
        rgba(255, 255, 255, 0.03)
    );
    padding: 20px;
    border-radius: 16px;
    border: 1px solid rgba(255, 255, 255, 0.12);
    box-shadow: 0 4px 15px rgba(0, 0, 0, 0.15);
    min-height: 110px;
}

[data-testid="stMetricLabel"] {
    font-size: 15px;
    font-weight: 600;
}

[data-testid="stMetricValue"] {
    font-size: 28px;
    font-weight: 700;
}

[data-testid="stSidebar"] {
    padding-top: 1rem;
}

.stButton > button {
    border-radius: 8px;
    font-weight: 600;
}

</style>
""", unsafe_allow_html=True)

# -----------------------------
# Load Data
# -----------------------------

df = pd.read_csv("data/expenses.csv")

df["Date"] = pd.to_datetime(df["Date"])

# -----------------------------
# Title
# -----------------------------

st.markdown(
    """
    <div style="padding: 10px 0 25px 0;">
        <h1 style="margin-bottom: 5px;">
            💰 Personal Expense Analytics Dashboard
        </h1>
        <p style="font-size: 18px; color: #9aa0a6;">
            Track, analyze, and understand your personal spending patterns
        </p>
    </div>
    """,
    unsafe_allow_html=True
)
# -----------------------------
# Sidebar Filters
# -----------------------------

st.sidebar.header("🔎 Filters")
# Monthly Budget
st.sidebar.subheader("💰 Budget")

monthly_budget = st.sidebar.number_input(
    "Set Monthly Budget (₹)",
    min_value=1000,
    max_value=100000,
    value=15000,
    step=500
)

# Date filter
min_date = df["Date"].min().date()
max_date = df["Date"].max().date()

date_range = st.sidebar.date_input(
    "Select Date Range",
    [min_date, max_date],
    min_value=min_date,
    max_value=max_date
)

# Category filter
categories = st.sidebar.multiselect(
    "Select Category",
    options=sorted(df["Category"].unique()),
    default=sorted(df["Category"].unique())
)

# Payment method filter
payments = st.sidebar.multiselect(
    "Payment Method",
    options=sorted(df["Payment_Method"].unique()),
    default=sorted(df["Payment_Method"].unique())
)

# Necessity filter
necessity = st.sidebar.multiselect(
    "Necessity",
    options=sorted(df["Necessity"].unique()),
    default=sorted(df["Necessity"].unique())
)

# -----------------------------
# Apply Filters
# -----------------------------

filtered_df = df[
    (df["Category"].isin(categories)) &
    (df["Payment_Method"].isin(payments)) &
    (df["Necessity"].isin(necessity))
]

if len(date_range) == 2:
    filtered_df = filtered_df[
        (filtered_df["Date"].dt.date >= date_range[0]) &
        (filtered_df["Date"].dt.date <= date_range[1])
    ]
# -----------------------------
# Budget Calculation
# -----------------------------

current_month = filtered_df["Date"].dt.to_period("M").max()

current_month_expense = filtered_df[
    filtered_df["Date"].dt.to_period("M") == current_month
]["Amount"].sum()

remaining_budget = monthly_budget - current_month_expense

budget_percentage = (
    current_month_expense / monthly_budget
) * 100
# -----------------------------
# Budget Status
# -----------------------------

st.subheader("💰 Monthly Budget Status")

st.progress(
    min(budget_percentage / 100, 1.0)
)

if budget_percentage < 75:
    st.success(
        f"✅ You have used {budget_percentage:.1f}% of your monthly budget."
    )

elif budget_percentage < 100:
    st.warning(
        f"⚠️ You have used {budget_percentage:.1f}% of your monthly budget."
    )

else:
    st.error(
        f"🚨 You have exceeded your monthly budget by "
        f"₹{abs(remaining_budget):,.0f}."
    )
    # -----------------------------
# Budget Summary
# -----------------------------

st.subheader("📊 Budget Summary")

budget_col1, budget_col2, budget_col3 = st.columns(3)

budget_col1.metric(
    "💰 Monthly Budget",
    f"₹{monthly_budget:,.0f}"
)

budget_col2.metric(
    "💸 Current Month Spending",
    f"₹{current_month_expense:,.0f}"
)

budget_col3.metric(
    "🟢 Remaining Budget",
    f"₹{remaining_budget:,.0f}"
)
# -----------------------------
# Top Spending Categories
# -----------------------------

st.subheader("🏆 Top Spending Categories")

top_categories = (
    filtered_df.groupby("Category")["Amount"]
    .sum()
    .sort_values(ascending=False)
    .head(5)
    .reset_index()
)

fig_top_categories = px.bar(
    top_categories,
    x="Amount",
    y="Category",
    orientation="h",
    title="Top 5 Spending Categories",
    text_auto=True
)

fig_top_categories.update_traces(
    texttemplate="₹%{x:,.0f}",
    textposition="outside"
)

fig_top_categories.update_layout(
    yaxis=dict(categoryorder="total ascending"),
    xaxis_title="Total Expense (₹)",
    yaxis_title="Category"
)

st.plotly_chart(
    fig_top_categories,
    use_container_width=True
)
# -----------------------------
# KPI Cards
# -----------------------------

total_expense = filtered_df["Amount"].sum()
average_expense = filtered_df["Amount"].mean()
highest_expense = filtered_df["Amount"].max()
number_transactions = len(filtered_df)

col1, col2, col3, col4, col5 = st.columns(5)
col5.metric(
    "💵 Remaining Budget",
    f"₹{remaining_budget:,.0f}"
)

col1.metric(
    "💰 Total Expense",
    f"₹{total_expense:,.0f}"
)

col2.metric(
    "📊 Average Expense",
    f"₹{average_expense:,.0f}"
)

col3.metric(
    "🔝 Highest Expense",
    f"₹{highest_expense:,.0f}"
)

col4.metric(
    "🧾 Transactions",
    number_transactions
)

st.divider()

# -----------------------------
# Charts
# -----------------------------

col1, col2 = st.columns(2)

# Category spending
category_data = (
    filtered_df
    .groupby("Category")["Amount"]
    .sum()
    .reset_index()
    .sort_values("Amount", ascending=False)
)

fig_category = px.bar(
    category_data,
    x="Category",
    y="Amount",
    title="💳 Spending by Category",
    text_auto=True
)

col1.plotly_chart(fig_category, use_container_width=True)
# -----------------------------
# Subcategory Spending Analysis
# -----------------------------

st.subheader("🔎 Spending by Subcategory")

subcategory_data = (
    filtered_df
    .groupby("Subcategory")["Amount"]
    .sum()
    .reset_index()
    .sort_values("Amount", ascending=False)
)

fig_subcategory = px.bar(
    subcategory_data,
    x="Subcategory",
    y="Amount",
    title="Spending by Subcategory",
    text_auto=True
)

fig_subcategory.update_traces(
    texttemplate="₹%{y:,.0f}",
    textposition="outside"
)

st.plotly_chart(
    fig_subcategory,
    use_container_width=True
)
# -----------------------------
# Location Spending Analysis
# -----------------------------

st.subheader("📍 Spending by Location")

location_data = (
    filtered_df
    .groupby("Location")["Amount"]
    .sum()
    .reset_index()
    .sort_values("Amount", ascending=False)
)

fig_location = px.bar(
    location_data,
    x="Location",
    y="Amount",
    title="Spending by Location",
    text_auto=True
)

fig_location.update_traces(
    texttemplate="₹%{y:,.0f}",
    textposition="outside"
)

st.plotly_chart(
    fig_location,
    use_container_width=True
)
# -----------------------------
# Day of Week Spending Analysis
# -----------------------------

st.subheader("📅 Spending by Day of Week")

day_data = filtered_df.copy()

day_data["Day"] = day_data["Date"].dt.day_name()

day_order = [
    "Monday",
    "Tuesday",
    "Wednesday",
    "Thursday",
    "Friday",
    "Saturday",
    "Sunday"
]

day_spending = (
    day_data
    .groupby("Day")["Amount"]
    .sum()
    .reindex(day_order)
    .reset_index()
)

fig_day = px.bar(
    day_spending,
    x="Day",
    y="Amount",
    title="Spending by Day of Week",
    text_auto=True
)

fig_day.update_traces(
    texttemplate="₹%{y:,.0f}",
    textposition="outside"
)

st.plotly_chart(
    fig_day,
    use_container_width=True
)
# -----------------------------
# Mood Spending Analysis
# -----------------------------

st.subheader("😊 Spending by Mood")

mood_data = (
    filtered_df
    .groupby("Mood")["Amount"]
    .sum()
    .reset_index()
    .sort_values("Amount", ascending=False)
)

fig_mood = px.bar(
    mood_data,
    x="Mood",
    y="Amount",
    title="Spending by Mood",
    text_auto=True
)

fig_mood.update_traces(
    texttemplate="₹%{y:,.0f}",
    textposition="outside"
)

st.plotly_chart(
    fig_mood,
    use_container_width=True
)

# Payment method
payment_data = (
    filtered_df
    .groupby("Payment_Method")["Amount"]
    .sum()
    .reset_index()
)

fig_payment = px.pie(
    payment_data,
    names="Payment_Method",
    values="Amount",
    title="💳 Spending by Payment Method"
)

col2.plotly_chart(fig_payment, use_container_width=True)



# -----------------------------
# Monthly Spending Analysis
# -----------------------------

st.subheader("📈 Monthly Spending Analysis")

monthly_data = (
    filtered_df
    .assign(Month=filtered_df["Date"].dt.to_period("M").astype(str))
    .groupby("Month")["Amount"]
    .sum()
    .reset_index()
)

# Calculate month-to-month change
monthly_data["Change"] = monthly_data["Amount"].pct_change() * 100

fig_monthly = px.line(
    monthly_data,
    x="Month",
    y="Amount",
    markers=True,
    title="📈 Monthly Spending Trend",
    text="Amount"
)

fig_monthly.update_traces(
    line_width=3,
    texttemplate="₹%{text:,.0f}",
    textposition="top center"
)

fig_monthly.update_layout(
    xaxis_title="Month",
    yaxis_title="Expense (₹)",
    hovermode="x unified"
)

fig_monthly.update_traces(
    texttemplate="₹%{text:,.0f}",
    textposition="top center"
)

st.plotly_chart(
    fig_monthly,
    use_container_width=True
)

# -----------------------------
# Monthly Comparison Table
# -----------------------------

st.subheader("📊 Monthly Spending Comparison")

# -----------------------------
# Monthly Comparison Table
# -----------------------------

comparison_data = monthly_data.copy()

# Calculate month-to-month change
comparison_data["Change"] = (
    comparison_data["Amount"].pct_change() * 100
)

comparison_data["Amount"] = comparison_data["Amount"].round(2)
comparison_data["Change"] = comparison_data["Change"].round(2)

comparison_data["Change"] = comparison_data["Change"].apply(
    lambda x: f"{x:+.2f}%" if pd.notna(x) else "-"
)

comparison_data = comparison_data.rename(
    columns={
        "Month": "Month",
        "Amount": "Total Expense (₹)",
        "Change": "Month-to-Month Change"
    }
)

st.dataframe(
    comparison_data,
    use_container_width=True,
    hide_index=True
)

# -----------------------------
# Necessity Analysis
# -----------------------------

necessity_data = (
    filtered_df
    .groupby("Necessity")["Amount"]
    .sum()
    .reset_index()
)

fig_necessity = px.bar(
    necessity_data,
    x="Necessity",
    y="Amount",
    title="🎯 Necessary vs Non-Necessary Spending",
    text_auto=True
)

st.plotly_chart(fig_necessity, use_container_width=True)

# -----------------------------
# Detailed Transactions
# -----------------------------

st.subheader("📋 Expense Transactions")

st.dataframe(
    filtered_df.sort_values("Date", ascending=False),
    use_container_width=True
)

# -----------------------------
# Summary
# -----------------------------

st.subheader("💡 Quick Insights")

if not filtered_df.empty:

    top_category = (
        filtered_df.groupby("Category")["Amount"]
        .sum()
        .idxmax()
    )

    top_category_amount = (
        filtered_df.groupby("Category")["Amount"]
        .sum()
        .max()
    )

    st.write(
        f"• Your highest spending category is **{top_category}** "
        f"with **₹{top_category_amount:,.0f}**."
    )

    # -----------------------------
# Automatic Spending Insights
# -----------------------------

st.subheader("🧠 Automatic Spending Insights")

if len(filtered_df) > 0:

    # Highest spending category
    category_spending = (
        filtered_df.groupby("Category")["Amount"]
        .sum()
        .sort_values(ascending=False)
    )

    top_category = category_spending.index[0]
    top_category_amount = category_spending.iloc[0]

    # Most used payment method
    payment_usage = filtered_df["Payment_Method"].value_counts()
    top_payment = payment_usage.index[0]

    # Necessary vs non-necessary
    necessary_amount = filtered_df[
        filtered_df["Necessity"] == "Yes"
    ]["Amount"].sum()

    non_necessary_amount = filtered_df[
        filtered_df["Necessity"] == "No"
    ]["Amount"].sum()

    # Average transaction
    average_transaction = filtered_df["Amount"].mean()

    col1, col2 = st.columns(2)

    with col1:
        st.info(
            f"💡 **Top Spending Category:** {top_category} "
            f"with ₹{top_category_amount:,.0f}"
        )

        st.info(
            f"💳 **Most Used Payment Method:** {top_payment}"
        )

    with col2:
        st.info(
            f"📊 **Average Transaction:** "
            f"₹{average_transaction:,.0f}"
        )

        st.info(
            f"🛍️ **Non-Necessary Spending:** "
            f"₹{non_necessary_amount:,.0f}"
        )


# -----------------------------
# Unusual Spending Detection
# -----------------------------

st.subheader("🚨 Unusual Spending Detection")

average_amount = filtered_df["Amount"].mean()
std_amount = filtered_df["Amount"].std()

threshold = average_amount + (2 * std_amount)

unusual_expenses = filtered_df[
    filtered_df["Amount"] > threshold
].sort_values(
    by="Amount",
    ascending=False
)

if len(unusual_expenses) > 0:

    st.warning(
        f"Found {len(unusual_expenses)} unusually high transactions."
    )

    st.dataframe(
        unusual_expenses[
            [
                "Date",
                "Category",
                "Subcategory",
                "Description",
                "Amount",
                "Payment_Method",
                "Necessity"
            ]
        ],
        use_container_width=True,
        hide_index=True
    )

else:

    st.success("✅ No unusually high transactions detected.")
    # -----------------------------
# Transaction Explorer
# -----------------------------

st.subheader("🔎 Transaction Explorer")

search_text = st.text_input(
    "Search transactions",
    placeholder="Search by description..."
)

explorer_df = filtered_df.copy()

if search_text:
    explorer_df = explorer_df[
        explorer_df["Description"]
        .str.contains(search_text, case=False, na=False)
    ]

subcategory_options = sorted(
    explorer_df["Subcategory"].unique()
)

selected_subcategories = st.multiselect(
    "Select Subcategory",
    subcategory_options
)

if selected_subcategories:
    explorer_df = explorer_df[
        explorer_df["Subcategory"].isin(
            selected_subcategories
        )
    ]

sort_order = st.selectbox(
    "Sort Transactions By",
    [
        "Newest First",
        "Oldest First",
        "Highest Amount",
        "Lowest Amount"
    ]
)

if sort_order == "Newest First":
    explorer_df = explorer_df.sort_values(
        "Date",
        ascending=False
    )

elif sort_order == "Oldest First":
    explorer_df = explorer_df.sort_values(
        "Date",
        ascending=True
    )

elif sort_order == "Highest Amount":
    explorer_df = explorer_df.sort_values(
        "Amount",
        ascending=False
    )

elif sort_order == "Lowest Amount":
    explorer_df = explorer_df.sort_values(
        "Amount",
        ascending=True
    )

st.write(
    f"Showing **{len(explorer_df)} transactions**"
)

st.dataframe(
    explorer_df[
        [
            "Date",
            "Category",
            "Subcategory",
            "Description",
            "Amount",
            "Payment_Method",
            "Necessity",
            "Location",
            "Mood"
        ]
    ],
    use_container_width=True,
    hide_index=True
)
    # -----------------------------
# Download Filtered Data
# -----------------------------

st.subheader("📥 Download Filtered Data")

csv_data = filtered_df.to_csv(index=False).encode("utf-8")

st.download_button(
    label="📥 Download CSV",
    data=csv_data,
    file_name="filtered_expenses.csv",
    mime="text/csv"
)