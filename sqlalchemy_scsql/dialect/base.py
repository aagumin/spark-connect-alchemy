from sqlalchemy.engine import default

from sqlalchemy_scsql.dbapi import dbapi

class SparkConnectDialect(default.DefaultDialect):
    """This dialect implements only those methods required to pass our e2e tests"""

    # Possible attributes are defined here: https://docs.sqlalchemy.org/en/14/core/internals.html#sqlalchemy.engine.Dialect
    name: str = "sc"
    driver: str = "sc"
    default_schema_name: str = "default"

    supports_statement_cache: bool = True
    supports_multivalues_insert: bool = True
    supports_native_decimal: bool = True
    supports_sane_rowcount: bool = False
    non_native_boolean_check_constraint: bool = False

    @classmethod
    def dbapi(cls):
        return dbapi
