# Databricks notebook source
# MAGIC %md
# MAGIC # 02 — Transform Silver (clean & standardize)

# COMMAND ----------

CATALOG = "main"
SCHEMA = "supply_chain"

# COMMAND ----------

spark.sql(f"""
CREATE OR REPLACE TABLE {CATALOG}.{SCHEMA}.orders_clean AS
SELECT
    CAST(`Order Id` AS BIGINT)                         AS order_id,
    CAST(`Order Item Id` AS BIGINT)                  AS order_item_id,
    CAST(`Customer Id` AS BIGINT)                      AS customer_id,
    CAST(`Order Customer Id` AS BIGINT)                AS order_customer_id,
    TRIM(`Customer Fname`)                             AS customer_fname,
    TRIM(`Customer Segment`)                           AS customer_segment,
    TRIM(`Customer City`)                              AS customer_city,
    TRIM(`Customer State`)                             AS customer_state,
    TRIM(`Customer Country`)                           AS customer_country,
    TRY_TO_TIMESTAMP(`order date (DateOrders)`)        AS order_date,
    TRY_TO_TIMESTAMP(`shipping date (DateOrders)`)     AS ship_date,
    TRIM(`Type`)                                       AS payment_type,
    TRIM(`Delivery Status`)                            AS delivery_status,
    CAST(`Late_delivery_risk` AS INT)                  AS late_delivery_risk,
    CAST(`Days for shipping (real)` AS DOUBLE)         AS days_shipping_actual,
    CAST(`Days for shipment (scheduled)` AS DOUBLE)    AS days_shipping_scheduled,
    TRIM(`Shipping Mode`)                              AS shipping_mode,
    TRIM(`Market`)                                     AS market,
    TRIM(`Order Region`)                               AS order_region,
    TRIM(`Order Country`)                              AS order_country,
    TRIM(`Order State`)                                AS order_state,
    TRIM(`Order City`)                                 AS order_city,
    TRIM(`Department Name`)                            AS department,
    TRIM(`Category Name`)                              AS category,
    TRIM(`Product Name`)                               AS product_name,
    TRIM(`Order Status`)                               AS order_status,
    CAST(`Sales` AS DOUBLE)                            AS sales,
    CAST(`Order Profit Per Order` AS DOUBLE)           AS profit,
    CAST(`Order Item Discount Rate` AS DOUBLE)         AS discount_rate,
    CAST(`Order Item Quantity` AS INT)                 AS quantity,
    CAST(`Benefit per order` AS DOUBLE)                AS benefit_per_order,
    CAST(`Sales per customer` AS DOUBLE)               AS sales_per_customer
FROM {CATALOG}.{SCHEMA}.orders_raw
""")

# COMMAND ----------

display(spark.table(f"{CATALOG}.{SCHEMA}.orders_clean").limit(5))
print(f"Silver rows: {spark.table(f'{CATALOG}.{SCHEMA}.orders_clean').count():,}")
