# Product Inventory Analytics Pipeline

End-to-end data pipeline that processes product inventory and sales data
using:

-   **Python (ETL with pandas)**
-   **Snowflake (cloud data warehouse)**
-   **Tableau Desktop + Tableau Cloud**
-   **Apache Airflow (orchestration)**
-   **SQL**
-   **Data Warehouse Modeling**

------------------------------------------------------------------------

## 🧱 Architecture Overview

    Raw CSVs (sales.csv, inventory.csv)
              │
              ▼
       Python ETL (pandas)
              │
              ▼
     Clean CSV outputs (clean_sales_inventory.csv, agg_sales_by_product.csv)
              │
              ▼
     Snowflake (INVENTORY_PROJECT.ANALYTICS)
          ├─ STAGING_SALES_INVENTORY
          ├─ DIM_PRODUCT
          └─ FACT_SALES
              │
              ▼
     Tableau Desktop → Tableau Cloud
              │
              ▼
     Apache Airflow DAG (@daily ETL)

------------------------------------------------------------------------

## 📂 Project Structure

    project-root/
    ├─ etl_inventory_sales.py
    ├─ inventory.csv
    ├─ sales.csv
    ├─ clean_sales_inventory.csv
    ├─ agg_sales_by_product.csv
    ├─ inventory_status.csv
    ├─ airflow/
    │  └─ dags/
    │     └─ inventory_etl_dag.py
    └─ README.md

------------------------------------------------------------------------

## 🧹 Python ETL Script

**etl_inventory_sales.py** performs:

1.  Load `inventory.csv` & `sales.csv`
2.  Clean and normalize data
3.  Join datasets using product ID
4.  Compute:
    -   `revenue = quantity * unit_price`
    -   `cost = quantity * unit_cost`
    -   `profit = revenue - cost`
5.  Export cleaned and aggregated CSVs

Run locally:

``` bash
python3 etl_inventory_sales.py
```

------------------------------------------------------------------------

## ❄️ Snowflake Warehouse

**Database:** `INVENTORY_PROJECT`\
**Schema:** `ANALYTICS`

### Tables Created

-   `STAGING_SALES_INVENTORY` -- cleansed data feed\
-   `DIM_PRODUCT` -- unique product attributes\
-   `FACT_SALES` -- revenue, cost, profit metrics

Example SQL:

``` sql
CREATE OR REPLACE TABLE dim_product AS
SELECT DISTINCT
    product_id,
    product_name,
    category,
    unit_cost,
    stock_on_hand,
    reorder_level
FROM staging_sales_inventory;
```

Revenue & profit query:

``` sql
SELECT
    p.product_name,
    SUM(f.quantity) AS total_qty,
    SUM(f.revenue)  AS total_revenue,
    SUM(f.profit)   AS total_profit
FROM fact_sales f
JOIN dim_product p USING (product_id)
GROUP BY p.product_name
ORDER BY total_revenue DESC;
```

------------------------------------------------------------------------

## 📊 Tableau Dashboard

Dashboard includes:

-   Revenue by Product\
-   Profit by Category\
-   Low-Stock / At-Risk Products\
-   Estimated stock after sales

Published publicly via Tableau Cloud.

------------------------------------------------------------------------

## 🌀 Apache Airflow Orchestration (v3.x)

DAG: **inventory_etl**

Runs daily and executes the ETL script.

``` python
run_etl = BashOperator(
    task_id="run_python_etl",
    bash_command=(
        'cd "/Users/<your-username>/airflow" && '
        'python3 etl_inventory_sales.py'
    ),
)
```

------------------------------------------------------------------------

## 🧰 Tech Stack

-   Python\
-   Pandas\
-   Snowflake\
-   SQL\
-   Tableau\
-   Apache Airflow\
-   macOS

------------------------------------------------------------------------

## 🚀 Future Enhancements

-   Load ETL output directly into Snowflake via Snowflake Python
    Connector\
-   Add Slack or email alerts in Airflow\
-   Parameterize ETL run dates\
-   Add store-wise performance dashboard

------------------------------------------------------------------------

## 📝 Author

Nehal Pawar --- Data Engineering & Analytics Portfolio
