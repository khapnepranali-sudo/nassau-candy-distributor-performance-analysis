import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# Create visuals folder automatically
os.makedirs("visuals", exist_ok=True)

df = pd.read_csv("data/Nassau Candy Distributor.csv")

print(df.info())

print("\nMissing Values:")
print(df.isnull().sum())

print("\nDuplicate Rows:")
print(df.duplicated().sum())

# Gross Margin %

df["Gross Margin %"] = (
    df["Gross Profit"] /
    df["Sales"]
) * 100

# Profit Per Unit

df["Profit Per Unit"] = (
    df["Gross Profit"] /
    df["Units"]
)

print(df[[
    "Product Name",
    "Sales",
    "Gross Profit",
    "Gross Margin %",
    "Profit Per Unit"
]].head())

# Product analysis
product_summary = df.groupby(
    "Product Name"
).agg(
    Sales=("Sales", "sum"),
    Profit=("Gross Profit", "sum"),
    Cost=("Cost", "sum"),
    Units=("Units", "sum")
)

product_summary["Margin %"] = (
    product_summary["Profit"] /
    product_summary["Sales"]
) * 100

print(product_summary.sort_values(
    "Profit",
    ascending=False
))

# Charts
product_summary = df.groupby(
    "Product Name"
).agg(
    Profit=("Gross Profit", "sum")
)

top10 = product_summary.sort_values(
    "Profit",
    ascending=False
).head(10)

plt.figure(figsize=(12,6))

sns.barplot(
    x=top10["Profit"],
    y=top10.index
)

plt.title("Top 10 Products By Profit")

plt.tight_layout()
plt.savefig(
    "visuals/top10_products_profit.png",
    dpi=300,
    bbox_inches="tight"
)

plt.show()

# Division Analysis
division_summary = df.groupby("Division").agg(
    Revenue=("Sales", "sum"),
    Profit=("Gross Profit", "sum"),
    Cost=("Cost", "sum"),
    Units=("Units", "sum")
)

division_summary["Margin %"] = (
    division_summary["Profit"] /
    division_summary["Revenue"]
) * 100

print(division_summary)

# Division  Charts
division_summary = df.groupby("Division").agg(
    Revenue=("Sales","sum"),
    Profit=("Gross Profit","sum")
)

division_summary.plot(
    kind="bar",
    figsize=(10,5)
)

plt.title("Revenue vs Profit by Division")
plt.ylabel("Amount")
plt.tight_layout()
plt.savefig(
    "visuals/division_revenue_profit.png",
    dpi=300,
    bbox_inches="tight"
)
plt.show()

# Pareto products summary
product_summary = df.groupby(
    "Product Name"
).agg(
    Profit=("Gross Profit","sum")
).reset_index()

product_summary = product_summary.sort_values(
    "Profit",
    ascending=False
)

product_summary["Cumulative Profit"] = (
    product_summary["Profit"].cumsum()
)

product_summary["Cumulative Profit %"] = (
    product_summary["Cumulative Profit"] /
    product_summary["Profit"].sum()
) * 100

print(product_summary)
pareto_80 = product_summary[
    product_summary["Cumulative Profit %"] <= 80
]

print("\nProducts contributing to first 80% profit:")
print(pareto_80[["Product Name", "Profit"]])
fig, ax1 = plt.subplots(figsize=(12,6))

ax1.bar(
    product_summary["Product Name"],
    product_summary["Profit"]
)

ax1.set_ylabel("Profit")
ax1.tick_params(axis="x", rotation=90)

ax2 = ax1.twinx()

ax2.plot(
    product_summary["Cumulative Profit %"],
    color="red",
    marker="o"
)

ax2.axhline(
    80,
    color="green",
    linestyle="--"
)

ax2.set_ylabel("Cumulative Profit %")

plt.title("Pareto Analysis - Product Profit")

plt.tight_layout()

plt.savefig(
    "visuals/pareto_analysis.png",
    dpi=300,
    bbox_inches="tight"
)

plt.show()


# Cost Profit
product_summary = df.groupby(
    "Product Name"
).agg(
    Cost=("Cost","sum"),
    Profit=("Gross Profit","sum"),
    Sales=("Sales","sum")
).reset_index()

plt.figure(figsize=(10,6))

sns.scatterplot(
    data=product_summary,
    x="Cost",
    y="Profit",
    size="Sales"
)

plt.title("Cost vs Profit Analysis")
plt.savefig(
    "visuals/cost_vs_profit.png",
    dpi=300,
    bbox_inches="tight"
)


plt.show()

# Margin trend 
df["Order Date"] = pd.to_datetime(
    df["Order Date"],
    dayfirst=True
)

monthly = df.groupby(
    pd.Grouper(
        key="Order Date",
        freq="ME"
    )
).agg(
    Sales=("Sales","sum"),
    Profit=("Gross Profit","sum")
)

monthly["Margin %"] = (
    monthly["Profit"] /
    monthly["Sales"]
) * 100

print(monthly)

monthly["Margin %"].plot(
    figsize=(12,5)
)

plt.title("Monthly Margin Trend")
plt.savefig(
    "visuals/monthly_margin_trend.png",
    dpi=300,
    bbox_inches="tight"
)

plt.show()


