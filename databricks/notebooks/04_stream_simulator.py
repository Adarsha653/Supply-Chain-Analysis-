# Databricks notebook source
# MAGIC %md
# MAGIC # 04 — Simulated order stream (optional demo)
# MAGIC Replays historical orders into a stream table for live-style dashboards.

# COMMAND ----------

CATALOG = "main"
SCHEMA = "supply_chain"
BATCH_SIZE = 500

# COMMAND ----------

spark.sql(f"""
CREATE TABLE IF NOT EXISTS {CATALOG}.{SCHEMA}.stream_events (
    event_time TIMESTAMP,
    order_id BIGINT,
    sales DOUBLE,
    profit DOUBLE,
    market STRING,
    shipping_mode STRING,
    late_delivery_risk INT
) USING DELTA
""")

# COMMAND ----------

from pyspark.sql import functions as F

stream_source = (
    spark.table(f"{CATALOG}.{SCHEMA}.fact_orders")
    .filter(F.col("order_date").isNotNull())
    .orderBy("order_date")
    .select(
        "order_id",
        "sales",
        "profit",
        "market",
        "shipping_mode",
        "late_delivery_risk",
    )
)

total = stream_source.count()
print(f"Streaming {total:,} rows in batches of {BATCH_SIZE}")

# COMMAND ----------

# Run one batch at a time — re-run this cell to simulate more "live" events.
already = spark.table(f"{CATALOG}.{SCHEMA}.stream_events").count()
batch = (
    stream_source.limit(already + BATCH_SIZE)
    .subtract(stream_source.limit(already))
    .withColumn("event_time", F.current_timestamp())
)

if batch.count() == 0:
    print("Stream complete — all rows emitted.")
else:
    batch.write.format("delta").mode("append").saveAsTable(
        f"{CATALOG}.{SCHEMA}.stream_events"
    )
    print(f"Emitted batch. Total stream events: {already + batch.count():,}")

display(spark.table(f"{CATALOG}.{SCHEMA}.stream_events").orderBy(F.desc("event_time")).limit(20))
