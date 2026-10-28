"""Retail order analysis. Run from the repository root: python python/analyze_retail.py"""
from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "retail_orders.csv"
OUT = ROOT / "outputs"
OUT.mkdir(exist_ok=True)

df = pd.read_csv(DATA, parse_dates=["Order_Date"])

# Basic data-quality checks
checks = {
    "row_count": len(df),
    "duplicate_order_ids": int(df["Order_ID"].duplicated().sum()),
    "missing_cells": int(df.isna().sum().sum()),
    "negative_quantity_rows": int((df["Quantity"] < 0).sum()),
    "revenue_formula_mismatches": int(
        ((df["Revenue_INR"] - df["Quantity"] * df["Unit_Price_INR"] *
          (1 - df["Discount_Pct"])).abs() > 0.02).sum()
    ),
}
pd.DataFrame([checks]).to_csv(OUT / "data_quality_checks.csv", index=False)

df["Profit_Margin_Pct"] = 100 * df["Profit_INR"] / df["Revenue_INR"].replace(0, pd.NA)
df["Order_Month"] = df["Order_Date"].dt.to_period("M").astype(str)
kpis = pd.DataFrame([{
    "Orders": df["Order_ID"].nunique(),
    "Units_Sold": int(df["Quantity"].sum()),
    "Revenue_INR": round(df["Revenue_INR"].sum(), 2),
    "Profit_INR": round(df["Profit_INR"].sum(), 2),
    "Profit_Margin_Pct": round(100 * df["Profit_INR"].sum() / df["Revenue_INR"].sum(), 2),
}])
kpis.to_csv(OUT / "overall_kpis.csv", index=False)

category = (df.groupby("Category", as_index=False)
            .agg(Revenue_INR=("Revenue_INR", "sum"),
                 Profit_INR=("Profit_INR", "sum"),
                 Units_Sold=("Quantity", "sum")))
category["Profit_Margin_Pct"] = 100 * category["Profit_INR"] / category["Revenue_INR"]
category.sort_values("Revenue_INR", ascending=False).to_csv(OUT / "category_kpis.csv", index=False)

monthly = (df.groupby("Order_Month", as_index=False)
           .agg(Revenue_INR=("Revenue_INR", "sum"), Profit_INR=("Profit_INR", "sum")))
monthly.to_csv(OUT / "monthly_kpis.csv", index=False)

# Charts are intentionally simple; improve titles/labels as part of the portfolio.
plt.figure(figsize=(10, 5))
plt.plot(monthly["Order_Month"], monthly["Revenue_INR"], marker="o")
plt.title("Monthly Revenue Trend")
plt.xlabel("Month")
plt.ylabel("Revenue (INR)")
plt.xticks(rotation=60, ha="right")
plt.tight_layout()
plt.savefig(OUT / "monthly_revenue.png", dpi=160)
plt.close()

plt.figure(figsize=(8, 5))
category.sort_values("Revenue_INR").plot(
    x="Category", y="Revenue_INR", kind="barh", legend=False, figsize=(8, 5)
)
plt.title("Revenue by Product Category")
plt.xlabel("Revenue (INR)")
plt.ylabel("")
plt.tight_layout()
plt.savefig(OUT / "revenue_by_category.png", dpi=160)
plt.close()

discount = (df.groupby("Discount_Pct", as_index=False)
            .agg(Revenue_INR=("Revenue_INR", "sum"), Profit_INR=("Profit_INR", "sum")))
discount["Profit_Margin_Pct"] = 100 * discount["Profit_INR"] / discount["Revenue_INR"]
discount.to_csv(OUT / "discount_analysis.csv", index=False)

plt.figure(figsize=(8, 5))
plt.plot(discount["Discount_Pct"] * 100, discount["Profit_Margin_Pct"], marker="o")
plt.title("Discount Level vs Profit Margin")
plt.xlabel("Discount (%)")
plt.ylabel("Profit margin (%)")
plt.tight_layout()
plt.savefig(OUT / "discount_vs_margin.png", dpi=160)
plt.close()

print("Analysis complete. Outputs saved to:", OUT)
print(kpis.to_string(index=False))
print("\nData quality checks:")
print(pd.DataFrame([checks]).to_string(index=False))
