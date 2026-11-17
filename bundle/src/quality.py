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
dbutils.widgets.text("join_type","left")
assert dbutils.widgets.get("join_type") in ("left","inner"), "Choose left or inner"
orders=spark.table(f"{silver}.orders")
assert orders.count()==4, "Run setup and transformations for this target first"
assert orders.filter("amount IS NULL OR amount < 0").count()==0
dbutils.jobs.taskValues.set(key="valid_rows",value=orders.count())
