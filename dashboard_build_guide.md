# Power BI dashboard build guide

## Import and model
1. Open Power BI Desktop → **Get data → Text/CSV** → select `retail_orders.csv`.
2. Set `Order_Date` to Date, numeric fields to Decimal Number/Whole Number, and `Discount_Pct` to Percentage.
3. This dataset is one row per order line; `Order_ID` is unique in this synthetic dataset. If you later model multi-line orders, count distinct order IDs rather than rows.
4. Create a Date table if you want proper time intelligence. Mark it as the date table and relate it to `retail_orders[Order_Date]`.

## Suggested DAX measures
```DAX
Total Revenue = SUM(retail_orders[Revenue_INR])

Total Profit = SUM(retail_orders[Profit_INR])

Profit Margin % = DIVIDE([Total Profit], [Total Revenue])

Total Orders = DISTINCTCOUNT(retail_orders[Order_ID])

Units Sold = SUM(retail_orders[Quantity])

Average Order Revenue = DIVIDE([Total Revenue], [Total Orders])
```
Format `Profit Margin %` as Percentage with 1 decimal place. Format revenue/profit as INR currency. Since `Profit Margin %` is a ratio, use the measure rather than averaging row-level margins.

## Page 1 — Executive overview
- KPI cards: Total Revenue, Total Profit, Profit Margin %, Total Orders.
- Line chart: Revenue by month.
- Bar chart: Revenue and profit by category.
- Slicers: Order Date, Region, Sales Channel.
- One sentence at the top: “Where is revenue growing, and is that growth profitable?”

## Page 2 — Product & discount analysis
- Matrix: Category → Product with Revenue, Profit, Margin %, Units Sold.
- Column chart: Profit by product.
- Scatter chart: Discount % vs Profit Margin % (size by Revenue).
- Slicer: Category.
- Use conditional formatting to highlight low-margin products.

## Page 3 — Region, channel & customer segment
- Bar chart: Profit by Region.
- Matrix: City and Region with Revenue, Profit, Margin %.
- Stacked column: Revenue by Sales Channel and Customer Segment.
- Slicers: Region, Customer Segment, Sales Channel.

## Design rules
- Keep a consistent 2–3 colour palette and generous whitespace.
- Use clear titles and INR units; avoid 3D charts.
- Add tooltips for profit and margin.
- Make every chart answer a business question; remove visuals that do not support a decision.
- Take screenshots of each finished page and add them to `powerbi/screenshots/` before publishing to GitHub.

## Final QA
- Check totals against `outputs/overall_kpis.csv` from Python.
- Test slicers and cross-filtering.
- Verify profit margin uses `Total Profit / Total Revenue`, not average of row margins.
- Add alt text to important visuals and ensure text remains readable.
