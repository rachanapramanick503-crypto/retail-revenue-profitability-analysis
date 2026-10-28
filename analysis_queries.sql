-- Retail Revenue & Profitability Analysis
-- Import retail_orders.csv into a MySQL table named retail_orders first.
-- Monetary values are INR. Discount_Pct is stored as a decimal (e.g. 0.15 = 15%).

-- 1) Overall KPI snapshot
SELECT
  COUNT(DISTINCT Order_ID) AS total_orders,
  SUM(Quantity) AS units_sold,
  ROUND(SUM(Revenue_INR), 2) AS revenue_inr,
  ROUND(SUM(Profit_INR), 2) AS profit_inr,
  ROUND(100 * SUM(Profit_INR) / NULLIF(SUM(Revenue_INR), 0), 2) AS profit_margin_pct
FROM retail_orders;

-- 2) Revenue and profit by category
SELECT Category, ROUND(SUM(Revenue_INR),2) AS revenue_inr,
       ROUND(SUM(Profit_INR),2) AS profit_inr,
       ROUND(100*SUM(Profit_INR)/NULLIF(SUM(Revenue_INR),0),2) AS margin_pct
FROM retail_orders GROUP BY Category ORDER BY revenue_inr DESC;

-- 3) Top 10 products by profit
SELECT Product, Category, SUM(Quantity) AS units_sold,
       ROUND(SUM(Revenue_INR),2) AS revenue_inr,
       ROUND(SUM(Profit_INR),2) AS profit_inr
FROM retail_orders GROUP BY Product, Category
ORDER BY profit_inr DESC LIMIT 10;

-- 4) Monthly revenue and profit trend
SELECT DATE_FORMAT(Order_Date, '%Y-%m') AS order_month,
       ROUND(SUM(Revenue_INR),2) AS revenue_inr,
       ROUND(SUM(Profit_INR),2) AS profit_inr
FROM retail_orders GROUP BY DATE_FORMAT(Order_Date, '%Y-%m')
ORDER BY order_month;

-- 5) Regional performance
SELECT Region, COUNT(DISTINCT Order_ID) AS orders,
       ROUND(SUM(Revenue_INR),2) AS revenue_inr,
       ROUND(SUM(Profit_INR),2) AS profit_inr,
       ROUND(100*SUM(Profit_INR)/NULLIF(SUM(Revenue_INR),0),2) AS margin_pct
FROM retail_orders GROUP BY Region ORDER BY profit_inr DESC;

-- 6) Sales channel comparison
SELECT Sales_Channel, COUNT(DISTINCT Order_ID) AS orders,
       ROUND(SUM(Revenue_INR),2) AS revenue_inr,
       ROUND(SUM(Profit_INR),2) AS profit_inr,
       ROUND(100*SUM(Profit_INR)/NULLIF(SUM(Revenue_INR),0),2) AS margin_pct
FROM retail_orders GROUP BY Sales_Channel ORDER BY revenue_inr DESC;

-- 7) Discount band analysis: check whether larger discounts coincide with weaker margins
SELECT CASE
         WHEN Discount_Pct = 0 THEN '0%'
         WHEN Discount_Pct <= 0.05 THEN '1–5%'
         WHEN Discount_Pct <= 0.10 THEN '6–10%'
         WHEN Discount_Pct <= 0.15 THEN '11–15%'
         ELSE 'Above 15%'
       END AS discount_band,
       COUNT(*) AS order_lines,
       ROUND(SUM(Revenue_INR),2) AS revenue_inr,
       ROUND(SUM(Profit_INR),2) AS profit_inr,
       ROUND(100*SUM(Profit_INR)/NULLIF(SUM(Revenue_INR),0),2) AS margin_pct
FROM retail_orders
GROUP BY discount_band
ORDER BY MIN(Discount_Pct);

-- 8) Customer segment contribution
SELECT Customer_Segment, COUNT(DISTINCT Order_ID) AS orders,
       ROUND(SUM(Revenue_INR),2) AS revenue_inr,
       ROUND(SUM(Profit_INR),2) AS profit_inr
FROM retail_orders GROUP BY Customer_Segment ORDER BY revenue_inr DESC;

-- 9) Cities with high revenue but below-average margin
WITH city_kpis AS (
  SELECT City, Region, SUM(Revenue_INR) AS revenue_inr,
         SUM(Profit_INR) AS profit_inr,
         100*SUM(Profit_INR)/NULLIF(SUM(Revenue_INR),0) AS margin_pct
  FROM retail_orders GROUP BY City, Region
),
overall AS (
  SELECT 100*SUM(Profit_INR)/NULLIF(SUM(Revenue_INR),0) AS overall_margin_pct
  FROM retail_orders
)
SELECT c.City, c.Region, ROUND(c.revenue_inr,2) AS revenue_inr,
       ROUND(c.profit_inr,2) AS profit_inr, ROUND(c.margin_pct,2) AS margin_pct
FROM city_kpis c CROSS JOIN overall o
WHERE c.margin_pct < o.overall_margin_pct
ORDER BY c.revenue_inr DESC;

-- 10) Monthly revenue change (month-over-month)
WITH monthly AS (
  SELECT DATE_FORMAT(Order_Date, '%Y-%m') AS order_month,
         SUM(Revenue_INR) AS revenue_inr
  FROM retail_orders
  GROUP BY DATE_FORMAT(Order_Date, '%Y-%m')
),
lagged AS (
  SELECT order_month, revenue_inr,
         LAG(revenue_inr) OVER (ORDER BY order_month) AS previous_month_revenue
  FROM monthly
)
SELECT order_month, ROUND(revenue_inr,2) AS revenue_inr,
       ROUND(previous_month_revenue,2) AS previous_month_revenue,
       ROUND(100*(revenue_inr-previous_month_revenue)/NULLIF(previous_month_revenue,0),2) AS mom_change_pct
FROM lagged ORDER BY order_month;

-- Optional data quality checks
SELECT COUNT(*) AS row_count,
       SUM(Order_ID IS NULL) AS missing_order_ids,
       SUM(Order_Date IS NULL) AS missing_dates,
       SUM(Revenue_INR < 0) AS negative_revenue_rows,
       SUM(Profit_INR > Revenue_INR) AS suspicious_profit_rows
FROM retail_orders;
