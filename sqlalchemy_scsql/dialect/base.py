from sqlalchemy.engine import default

from sqlalchemy_scsql.dbapi import dbapi

class SparkConnectDialect(default.DefaultDialect):
    name = 'sc'
    dbapi = dbapi
    @classmethod
    def import_dbapi(cls):
        return dbapi

    def get_table_names(self, connection, schema=None, **kw):
        pass

    def get_view_names(self, connection, schema=None, **kw):
        pass

    def get_columns(self, connection, table_name, schema=None, **kw):
        pass
    # Define any necessary methods and properties here
