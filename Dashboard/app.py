import streamlit as st
import pandas as pd
import plotly.express as px

# Page Config
st.set_page_config(
    page_title="Nassau Candy Profitability Dashboard",
    layout="wide"
)

st.title(" Nassau Candy Distributor Performance Analysis")

# Load Data
df = pd.read_csv("data/Nassau Candy Distributor.csv")

# KPI Calculations
df["Gross Margin %"] = (
    df["Gross Profit"] / df["Sales"]
) * 100

df["Profit Per Unit"] = (
    df["Gross Profit"] / df["Units"]
)

# Sidebar Filters
st.sidebar.header("Filters")

division = st.sidebar.multiselect(
    "Select Division",
    options=df["Division"].unique(),
    default=df["Division"].unique()
)

df = df[df["Division"].isin(division)]

# KPIs
total_sales = df["Sales"].sum()
total_profit = df["Gross Profit"].sum()
avg_margin = df["Gross Margin %"].mean()

col1, col2, col3 = st.columns(3)

col1.metric("Total Sales", f"${total_sales:,.2f}")
col2.metric("Total Profit", f"${total_profit:,.2f}")
col3.metric("Average Margin %", f"{avg_margin:.2f}%")

st.divider()

# Product Profitability
st.subheader("Top 10 Products By Profit")

product_summary = df.groupby(
    "Product Name"
)["Gross Profit"].sum().reset_index()

product_summary = product_summary.sort_values(
    "Gross Profit",
    ascending=False
).head(10)

fig = px.bar(
    product_summary,
    x="Gross Profit",
    y="Product Name",
    orientation="h",
    title="Top Products By Profit"
)

st.plotly_chart(fig, use_container_width=True)

# Division Analysis
st.subheader("Division Performance")

division_summary = df.groupby(
    "Division"
).agg(
    Revenue=("Sales","sum"),
    Profit=("Gross Profit","sum")
).reset_index()

fig2 = px.bar(
    division_summary,
    x="Division",
    y=["Revenue","Profit"],
    barmode="group",
    title="Revenue vs Profit"
)

st.plotly_chart(fig2, use_container_width=True)

# Cost vs Profit
st.subheader("Cost vs Profit Analysis")

cost_profit = df.groupby(
    "Product Name"
).agg(
    Cost=("Cost","sum"),
    Profit=("Gross Profit","sum"),
    Sales=("Sales","sum")
).reset_index()

fig3 = px.scatter(
    cost_profit,
    x="Cost",
    y="Profit",
    size="Sales",
    hover_name="Product Name",
    title="Cost vs Profit Scatter"
)

st.plotly_chart(fig3, use_container_width=True)

# Product Table
st.subheader("Product Summary")

st.dataframe(cost_profit)