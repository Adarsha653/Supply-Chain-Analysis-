# Databricks notebook source
# MAGIC %md
# MAGIC # 02 — Transform Silver (clean & standardize, **all columns retained**)

# COMMAND ----------

CATALOG = "main"
SCHEMA = "supply_chain"

# COMMAND ----------

spark.sql(f"""
CREATE OR REPLACE TABLE {CATALOG}.{SCHEMA}.orders_clean AS
SELECT
    TRIM(`Type`)                                       AS type,
    CAST(`Days for shipping (real)` AS DOUBLE)         AS days_shipping_real,
    CAST(`Days for shipment (scheduled)` AS DOUBLE)    AS days_shipping_scheduled,
    CAST(`Benefit per order` AS DOUBLE)                AS benefit_per_order,
    CAST(`Sales per customer` AS DOUBLE)                 AS sales_per_customer,
    TRIM(`Delivery Status`)                            AS delivery_status,
    CAST(`Late_delivery_risk` AS INT)                  AS late_delivery_risk,
    CAST(`Category Id` AS INT)                         AS category_id,
    TRIM(`Category Name`)                              AS category_name,
    TRIM(`Customer City`)                              AS customer_city,
    TRIM(`Customer Country`)                           AS customer_country,
    TRIM(`Customer Email`)                             AS customer_email,
    TRIM(`Customer Fname`)                             AS customer_fname,
    CAST(`Customer Id` AS BIGINT)                      AS customer_id,
    TRIM(`Customer Lname`)                             AS customer_lname,
    TRIM(`Customer Password`)                            AS customer_password,
    TRIM(`Customer Segment`)                           AS customer_segment,
    TRIM(`Customer State`)                             AS customer_state,
    TRIM(`Customer Street`)                            AS customer_street,
    TRIM(CAST(`Customer Zipcode` AS STRING))           AS customer_zipcode,
    CAST(`Department Id` AS INT)                       AS department_id,
    TRIM(`Department Name`)                            AS department_name,
    CAST(`Latitude` AS DOUBLE)                         AS latitude,
    CAST(`Longitude` AS DOUBLE)                        AS longitude,
    TRIM(`Market`)                                     AS market,
    TRIM(`Order City`)                                 AS order_city,
    TRIM(`Order Country`)                              AS order_country,
    CAST(`Order Customer Id` AS BIGINT)                AS order_customer_id,
    TRY_TO_TIMESTAMP(`order date (DateOrders)`)        AS order_date,
    CAST(`Order Id` AS BIGINT)                         AS order_id,
    CAST(`Order Item Cardprod Id` AS BIGINT)           AS order_item_cardprod_id,
    CAST(`Order Item Discount` AS DOUBLE)              AS order_item_discount,
    CAST(`Order Item Discount Rate` AS DOUBLE)         AS order_item_discount_rate,
    CAST(`Order Item Id` AS BIGINT)                    AS order_item_id,
    CAST(`Order Item Product Price` AS DOUBLE)         AS order_item_product_price,
    CAST(`Order Item Profit Ratio` AS DOUBLE)          AS order_item_profit_ratio,
    CAST(`Order Item Quantity` AS INT)                 AS order_item_quantity,
    CAST(`Sales` AS DOUBLE)                            AS sales,
    CAST(`Order Item Total` AS DOUBLE)                 AS order_item_total,
    CAST(`Order Profit Per Order` AS DOUBLE)           AS order_profit_per_order,
    TRIM(`Order Region`)                               AS order_region,
    TRIM(`Order State`)                                AS order_state,
    TRIM(`Order Status`)                               AS order_status,
    TRIM(CAST(`Order Zipcode` AS STRING))              AS order_zipcode,
    CAST(`Product Card Id` AS BIGINT)                  AS product_card_id,
    CAST(`Product Category Id` AS INT)                 AS product_category_id,
    TRIM(`Product Description`)                          AS product_description,
    TRIM(`Product Image`)                              AS product_image,
    TRIM(`Product Name`)                               AS product_name,
    CAST(`Product Price` AS DOUBLE)                    AS product_price,
    CAST(`Product Status` AS INT)                      AS product_status,
    TRY_TO_TIMESTAMP(`shipping date (DateOrders)`)     AS ship_date,
    TRIM(`Shipping Mode`)                              AS shipping_mode
FROM {CATALOG}.{SCHEMA}.orders_raw
""")

# COMMAND ----------

display(spark.table(f"{CATALOG}.{SCHEMA}.orders_clean").limit(5))
print(f"Silver rows: {spark.table(f'{CATALOG}.{SCHEMA}.orders_clean').count():,}")
print(f"Silver columns: {len(spark.table(f'{CATALOG}.{SCHEMA}.orders_clean').columns)}")
