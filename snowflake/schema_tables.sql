-- Snowflake schema setup
CREATE OR REPLACE DATABASE INVENTORY_PROJECT;
CREATE OR REPLACE SCHEMA INVENTORY_PROJECT.ANALYTICS;

-- Staging table
CREATE OR REPLACE TABLE INVENTORY_PROJECT.ANALYTICS.STAGING_SALES_INVENTORY (
    sale_id INTEGER,
    sale_date DATE,
    product_id INTEGER,
    product_name STRING,
    category STRING,
    quantity INTEGER,
    unit_price NUMBER(10,2),
    unit_cost NUMBER(10,2),
    revenue NUMBER(10,2),
    cost NUMBER(10,2),
    profit NUMBER(10,2),
    stock_on_hand INTEGER,
    reorder_level INTEGER
);

-- Dimension table
CREATE OR REPLACE TABLE INVENTORY_PROJECT.ANALYTICS.DIM_PRODUCT AS
SELECT DISTINCT
    product_id,
    product_name,
    category,
    unit_cost,
    stock_on_hand,
    reorder_level
FROM INVENTORY_PROJECT.ANALYTICS.STAGING_SALES_INVENTORY;

-- Fact table
CREATE OR REPLACE TABLE INVENTORY_PROJECT.ANALYTICS.FACT_SALES AS
SELECT
    sale_id,
    sale_date,
    product_id,
    quantity,
    unit_price,
    revenue,
    cost,
    profit
FROM INVENTORY_PROJECT.ANALYTICS.STAGING_SALES_INVENTORY;
