# import logging
#
# from pyspark.sql import SparkSession
#
# #
# # spark = SparkSession.builder.remote("sc://localhost:15002").getOrCreate()
# # print(type(SparkSession.getActiveSession()))
# #
# # spark.sql("SELECT 1 != 2").show()
#
# from scsql.dbapi import connect
#
# conn = connect()
# cursor = conn.cursor()
#
# # Выполняем SQL-запрос
# cursor.execute("show databases;")
#
# # Получаем и выводим результаты
# rows = cursor.fetchall()
# for row in rows:
#     print(row)
#
# # Закрываем курсор и соединение
# # cursor.close()
# conn.close()

from sqlalchemy import create_engine
from sqlalchemy.dialects import registry

registry.register("sc", "sqlalchemy_scsql.dialect", "SparkConnectDialect")
# Создание движка для подключения к PySpark Connect
engine = create_engine("sc://localhost:15002")

# Выполнение SQL-запроса через SQLAlchemy
with engine.connect() as connection:
    result = connection.execute("SELECT * FROM mirror_mirror_new")
    for row in result:
        print(row)
