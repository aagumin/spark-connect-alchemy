import logging

from pyspark.sql import SparkSession

# spark = (
#     SparkSession
#     .builder
#     .remote("sc://spark-connect.svc.cluster.local:15002")
#     .getOrCreate()
# )
# print(type(SparkSession.getActiveSession()))
#
# spark.catalog.listDatabases()

#
# from sqlalchemy_scsql.dbapi.dbapi import connect
# # Create and configure logger
# logging.basicConfig()
# # Creating an object
# logger=logging.getLogger()
#
# # Setting the threshold of logger to DEBUG
# logger.setLevel(logging.DEBUG)
# conn = connect(config={"a":"b"})
# cursor = conn.cursor()
#
# # Выполняем SQL-запрос
# cursor.execute("show databases;")
#
# # Получаем и выводим результаты
# rows = cursor.fetchall()
# for row in rows:
#     print(row)

# Закрываем курсор и соединение
# cursor.close()
# conn.close()
# from sqlalchemy_scsql.dbapi.dbapi import connect
# Create and configure logger
logging.basicConfig()
# Creating an object
logger=logging.getLogger()

# Setting the threshold of logger to DEBUG
logger.setLevel(logging.DEBUG)
from sqlalchemy import create_engine
from sqlalchemy.dialects import registry

registry.register("sc", "sqlalchemy_scsql.dialect", "SparkConnectDialect")
# Создание движка для подключения к PySpark Connect
engine = create_engine("sc://localhost:15002")
from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey
# metadata_obj = MetaData()
# users = Table(
#      "users",
#     metadata_obj,
#     Column("id", Integer, primary_key=True),
#     Column("name", String),
#     Column("fullname", String),
# )
# metadata_obj.create_all(engine)
# Выполнение SQL-запроса через SQLAlchemy
with engine.connect() as connection:
    result = connection.execute("SHOW DATABASES;")
    for row in result:
        print(row)
