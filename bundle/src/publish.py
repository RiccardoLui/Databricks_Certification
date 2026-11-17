# Databricks notebook source
# Official docs: https://docs.databricks.com/aws/en/jobs/dynamic-value-references
# https://docs.databricks.com/aws/en/jobs/task-values
# https://docs.databricks.com/aws/en/pyspark/reference/classes/dataframe/join
import re
from pyspark.sql import functions as F
for key, default in [("catalog","workspace"),("prefix","dea_riccardo")]:
    dbutils.widgets.text(key,default)
catalog=dbutils.widgets.get("catalog"); prefix=dbutils.widgets.get("prefix")
assert re.fullmatch(r"[A-Za-z_][A-Za-z0-9_]*",catalog)
assert re.fullmatch(r"[A-Za-z_][A-Za-z0-9_]*",prefix)
silver=f"{catalog}.{prefix}_silver"; gold=f"{catalog}.{prefix}_gold"

# COMMAND ----------
result=spark.table(f"{gold}.job_join_result")
(result.withColumn("country",F.coalesce("country",F.lit("UNKNOWN"))).groupBy("country")
 .agg(F.sum("amount").alias("revenue")).write.mode("overwrite").saveAsTable(f"{gold}.job_revenue"))
