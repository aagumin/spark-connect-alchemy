from databricks.sqlalchemy.base import DatabricksDialect


class SparkConnectDialect(DatabricksDialect):
    driver = "com.databricks.spark.csv"