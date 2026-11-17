# ADVANCED: add to a NEW pipeline with kit.cdc_source set to an existing feed.
# Feed schema: id INT, country STRING, seq LONG, op STRING; op DELETE is a tombstone.
# Official docs: https://docs.databricks.com/aws/en/ldp/cdc
from pyspark import pipelines as dp
from pyspark.sql.functions import col, expr

@dp.table(name="customer_changes")
def customer_changes():
    return spark.readStream.table(spark.conf.get("kit.cdc_source"))

dp.create_streaming_table(name="customers_scd2")
dp.create_auto_cdc_flow(
    target="customers_scd2", source="customer_changes", keys=["id"],
    sequence_by=col("seq"), apply_as_deletes=expr("op = 'DELETE'"),
    except_column_list=["op", "seq"], stored_as_scd_type=2)
