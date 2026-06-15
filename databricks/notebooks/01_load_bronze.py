# Databricks notebook source
# MAGIC %md
# MAGIC # 01 — Load Bronze (raw CSV)
# MAGIC Run this once after uploading the CSV to your workspace.

# COMMAND ----------

# Update this path after you upload the file (see README Step 4).
CSV_PATH = "/Volumes/main/default/supply_chain/DataCoSupplyChainDataset.csv"

CATALOG = "main"
SCHEMA = "supply_chain"
TABLE = "orders_raw"

# COMMAND ----------

spark.sql(f"CREATE SCHEMA IF NOT EXISTS {CATALOG}.{SCHEMA}")

# COMMAND ----------

raw_df = (
    spark.read.option("header", True)
    .option("encoding", "ISO-8859-1")
    .option("inferSchema", True)
    .csv(CSV_PATH)
)

display(raw_df.limit(5))
print(f"Row count: {raw_df.count():,}")

# COMMAND ----------

(
    raw_df.write.format("delta")
    .mode("overwrite")
    .option("overwriteSchema", "true")
    .saveAsTable(f"{CATALOG}.{SCHEMA}.{TABLE}")
)

print(f"Saved to {CATALOG}.{SCHEMA}.{TABLE}")
