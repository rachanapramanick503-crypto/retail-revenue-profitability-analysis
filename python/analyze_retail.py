import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

# Project paths
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_FILE = BASE_DIR / "retail_orders.csv"
OUTPUT_DIR = BASE_DIR / "outputs"
OUTPUT_DIR.mkdir(exist_ok=True)

# Load the dataset
df = pd.read_csv(DATA_FILE)
df["Order_Date"] = pd.to_datetime(df["Order_Date"])

# Overall business performance
total_orders = df["Order_ID"].nunique()
total_revenue = df["Revenue_INR"].sum()
total_profit = df["Profit_INR"].sum()
units_sold = df["Quantity"].sum()

profit_margin = (
    total_profit / total_revenue * 100
    if total_revenue != 0 else 0
)

print("RETAIL BUSINESS PERFORMANCE")
print("-" * 35)
print(f"Total orders: {total_orders:,}")
print(f"Units sold: {units_sold:,}")
print(f"Total revenue: ₹{total_revenue:,.2f}")
print(f"Total profit: ₹{total_profit:,.2f}")
print(f"Profit margin: {profit_margin:.2f}%")

# Revenue and profit by category
category_summary = (
    df.groupby("Category", as_index=False)
    .agg(
        Revenue_INR=("Revenue_INR", "sum"),
        Profit_INR=("Profit_INR", "sum")
    )
    .sort_values("Revenue_INR", ascending=False)
)

category_summary.to_csv(
    OUTPUT_DIR / "category_summary.csv", index=False
)

print("\nPERFORMANCE BY CATEGORY")
print(category_summary.to_string(index=False))

# Monthly business trends
df["Order_Month"] = df["Order_Date"].dt.to_period("M").astype(str)

monthly_summary = (
    df.groupby("Order_Month", as_index=False)
    .agg(
        Revenue_INR=("Revenue_INR", "sum"),
        Profit_INR=("Profit_INR", "sum")
    )
)

monthly_summary.to_csv(
    OUTPUT_DIR / "monthly_summary.csv", index=False
)

# Revenue by category chart
plt.figure(figsize=(9, 5))
plt.bar(
    category_summary["Category"],
    category_summary["Revenue_INR"]
)
plt.title("Revenue by Product Category")
plt.xlabel("Category")
plt.ylabel("Revenue (INR)")
plt.xticks(rotation=20)
plt.tight_layout()
plt.savefig(OUTPUT_DIR / "revenue_by_category.png", dpi=150)
plt.close()

# Monthly revenue trend chart
plt.figure(figsize=(10, 5))
plt.plot(
    monthly_summary["Order_Month"],
    monthly_summary["Revenue_INR"],
    marker="o"
)
plt.title("Monthly Revenue Trend")
plt.xlabel("Month")
plt.ylabel("Revenue (INR)")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig(OUTPUT_DIR / "monthly_revenue_trend.png", dpi=150)
plt.close()

# Export the overall summary
summary = pd.DataFrame([{
    "Total_Orders": total_orders,
    "Units_Sold": units_sold,
    "Total_Revenue_INR": round(total_revenue, 2),
    "Total_Profit_INR": round(total_profit, 2),
    "Profit_Margin_Pct": round(profit_margin, 2)
}])

summary.to_csv(OUTPUT_DIR / "business_summary.csv", index=False)

print("\nAnalysis complete!")
print(f"Output files saved to: {OUTPUT_DIR}")
