# Pipeline source; do not run as an interactive notebook.
# Official Databricks docs:
# https://docs.databricks.com/aws/en/ldp/developer/python-dev
# https://docs.databricks.com/aws/en/ldp/expectations
from pyspark import pipelines as dp
from pyspark.sql import functions as F
BRONZE = spark.conf.get("kit.bronze")

@dp.table(name="orders_valid")
@dp.expect_or_drop("positive_amount", "amount_num IS NOT NULL AND amount_num >= 0")
def orders_valid():
    return (spark.readStream.table(f"{BRONZE}.orders_raw")
            .withColumn("amount_num", F.expr("try_cast(amount AS DECIMAL(12,2))")))

@dp.materialized_view(name="order_metrics")
def order_metrics():
    return spark.read.table("orders_valid").agg(
        F.count("*").alias("valid_event_rows"), F.sum("amount_num").alias("event_amount"))
