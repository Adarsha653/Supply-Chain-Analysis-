# Databricks notebook source
# MAGIC %md
# MAGIC # 03 — Build Gold tables & KPI views

# COMMAND ----------

CATALOG = "main"
SCHEMA = "supply_chain"

# COMMAND ----------

spark.sql(f"""
CREATE OR REPLACE TABLE {CATALOG}.{SCHEMA}.fact_orders AS
SELECT *
FROM {CATALOG}.{SCHEMA}.orders_clean
""")

spark.sql(f"""
CREATE OR REPLACE TABLE {CATALOG}.{SCHEMA}.dim_customers AS
SELECT DISTINCT
    customer_id,
    customer_fname,
    customer_lname,
    customer_email,
    customer_segment,
    customer_city,
    customer_state,
    customer_country,
    customer_street,
    customer_zipcode
FROM {CATALOG}.{SCHEMA}.orders_clean
""")

spark.sql(f"""
CREATE OR REPLACE TABLE {CATALOG}.{SCHEMA}.dim_products AS
SELECT DISTINCT
    product_name,
    category_name,
    department_name,
    product_price,
    product_image
FROM {CATALOG}.{SCHEMA}.orders_clean
""")

# COMMAND ----------

spark.sql(f"""
CREATE OR REPLACE VIEW {CATALOG}.{SCHEMA}.v_executive_summary AS
SELECT
    COUNT(*)                              AS order_lines,
    COUNT(DISTINCT order_id)              AS orders,
    COUNT(DISTINCT customer_id)           AS customers,
    ROUND(SUM(sales), 2)                  AS total_sales,
    ROUND(SUM(order_profit_per_order), 2) AS total_profit,
    ROUND(AVG(late_delivery_risk), 4)     AS late_delivery_rate
FROM {CATALOG}.{SCHEMA}.fact_orders
""")

spark.sql(f"""
CREATE OR REPLACE VIEW {CATALOG}.{SCHEMA}.v_late_delivery_by_mode AS
SELECT
    shipping_mode,
    COUNT(*)                          AS order_lines,
    ROUND(AVG(late_delivery_risk), 4) AS late_rate,
    ROUND(AVG(days_shipping_real - days_shipping_scheduled), 2) AS avg_delay_days,
    ROUND(SUM(order_profit_per_order), 2) AS total_profit
FROM {CATALOG}.{SCHEMA}.fact_orders
GROUP BY shipping_mode
ORDER BY late_rate DESC
""")

spark.sql(f"""
CREATE OR REPLACE VIEW {CATALOG}.{SCHEMA}.v_profit_by_market AS
SELECT
    market,
    department_name,
    COUNT(DISTINCT order_id)          AS orders,
    ROUND(SUM(sales), 2)              AS revenue,
    ROUND(SUM(order_profit_per_order), 2) AS profit,
    ROUND(AVG(late_delivery_risk), 4) AS late_rate
FROM {CATALOG}.{SCHEMA}.fact_orders
GROUP BY market, department_name
ORDER BY revenue DESC
""")

spark.sql(f"""
CREATE OR REPLACE VIEW {CATALOG}.{SCHEMA}.v_customer_360 AS
SELECT
    customer_id,
    customer_segment,
    customer_country,
    COUNT(DISTINCT order_id)          AS order_count,
    ROUND(SUM(sales), 2)              AS total_revenue,
    ROUND(SUM(order_profit_per_order), 2) AS total_profit,
    ROUND(AVG(late_delivery_risk), 4) AS late_rate,
    MAX(order_date)                   AS last_order_date
FROM {CATALOG}.{SCHEMA}.fact_orders
GROUP BY customer_id, customer_segment, customer_country
""")

spark.sql(f"""
CREATE OR REPLACE VIEW {CATALOG}.{SCHEMA}.v_at_risk_customers AS
SELECT *
FROM {CATALOG}.{SCHEMA}.v_customer_360
WHERE total_revenue > 1000 AND late_rate > 0.5
ORDER BY total_revenue DESC
""")

spark.sql(f"""
CREATE OR REPLACE VIEW {CATALOG}.{SCHEMA}.v_monthly_trends AS
SELECT
    DATE_TRUNC('month', order_date) AS month,
    COUNT(DISTINCT order_id)      AS orders,
    ROUND(SUM(sales), 2)          AS revenue,
    ROUND(SUM(order_profit_per_order), 2) AS profit,
    ROUND(AVG(late_delivery_risk), 4) AS late_rate
FROM {CATALOG}.{SCHEMA}.fact_orders
WHERE order_date IS NOT NULL
GROUP BY DATE_TRUNC('month', order_date)
ORDER BY month
""")

# COMMAND ----------

display(spark.sql(f"SELECT * FROM {CATALOG}.{SCHEMA}.v_executive_summary"))
display(spark.sql(f"SELECT * FROM {CATALOG}.{SCHEMA}.v_late_delivery_by_mode"))
display(spark.sql(f"SELECT * FROM {CATALOG}.{SCHEMA}.v_at_risk_customers LIMIT 20"))
