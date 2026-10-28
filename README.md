# Retail Revenue & Profitability Analysis

**Portfolio project | Data Analyst / Business Analyst | SQL + Python + Power BI**

## Business problem
A retail business wants to understand what drives revenue and profit across product categories, regions, customer segments and sales channels. The goal is to identify where growth is healthy, where discounts may be hurting margins, and what actions the business should test next.

> **Data note:** `retail_orders.csv` is a synthetic, practice dataset created for this portfolio project. It does not represent a real company or real customers. Monetary values are in INR.

## Questions this project answers
1. Which categories and products generate the most revenue and profit?
2. Which regions and cities are underperforming?
3. Which sales channels have the strongest profit margins?
4. How do discounts relate to profit margin?
5. Which customer segments contribute most to revenue?
6. How does revenue and profit change month over month?
7. What practical actions should a sales manager test?

## Tools
- **SQL (MySQL 8+)** — business questions, aggregations, ranking, month-on-month analysis.
- **Python (pandas, matplotlib)** — data validation, derived metrics and exploratory analysis.
- **Power BI** — interactive business dashboard (build using the provided dashboard specification).
- **Git/GitHub** — version-controlled portfolio and documentation.

## Repository contents
- `retail_orders.csv` — 1,200 synthetic order-line records.
- `sql/analysis_queries.sql` — table creation and 10 analysis queries.
- `python/analyze_retail.py` — validation, KPI summary and chart generation.
- `powerbi/dashboard_build_guide.md` — page layout, measures and design guidance.
- `docs/insights_template.md` — fill this in after running the analysis and building the dashboard.
- `requirements.txt` — Python dependencies.

## Run it locally
1. Download/clone this repository.
2. Install Python 3.10+ and dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run:
   ```bash
   python python/analyze_retail.py
   ```
4. The script creates `outputs/` with a KPI summary CSV and three charts.
5. To use SQL, create a database in MySQL Workbench or your SQL client, then import `retail_orders.csv` into a table named `retail_orders` (or use the `CREATE TABLE` statement as a starting point). Run `sql/analysis_queries.sql`.
6. In Power BI Desktop, load `retail_orders.csv` and follow `powerbi/dashboard_build_guide.md`.

## Dashboard pages
- **Executive overview:** revenue, profit, profit margin, orders, revenue trend.
- **Product & discount analysis:** category/product performance, discount bands and margin.
- **Regional & channel performance:** region/city and channel comparisons, segment mix.

## Important: make this your project, not just a downloaded repo
Before adding this to your resume:
- Run the Python script yourself and inspect the output.
- Execute at least 5 SQL queries and explain what each one tells the business.
- Build the Power BI report and add screenshots to `powerbi/screenshots/`.
- Replace the insight template with **actual numbers from your run**; don't copy generic claims.
- Add a short section on limitations and 2–3 recommendations supported by your results.
- Be ready to explain one data-quality check, one SQL query, one DAX measure and one business recommendation in an interview.

## Suggested resume entry
**Retail Revenue & Profitability Analysis | SQL, Python, Power BI**
- Analysed 1,200 synthetic retail order records to evaluate revenue, profit margin, discounting, regional performance and customer segments.
- Wrote SQL aggregations and ranking queries to compare category, channel and regional KPIs; used pandas to validate data and generate exploratory summaries.
- Built an interactive Power BI dashboard with executive KPIs, monthly trends and product/region drill-downs. *(Use this bullet only after you have built the dashboard.)*

## Project extension ideas
1. Add a what-if discount scenario page.
2. Add a customer repeat-purchase analysis if you extend the dataset with customer IDs.
3. Create a one-page business memo with 3 recommendations and expected impact.
