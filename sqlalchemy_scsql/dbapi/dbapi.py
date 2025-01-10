import logging
from typing import Optional, Union, Dict, Any, List, TYPE_CHECKING

from pyspark.sql.connect.session import SparkSession
from urllib3.util import Url

from sqlalchemy_scsql.dbapi.constans import DEFAULT_CONNECT_PORT, DEFAULT_CONNECT_HOST, CONN_STRING_PARAMS
from sqlalchemy_scsql.dbapi.exceptions import DatabaseError, NotSupportedError, OperationalError

if TYPE_CHECKING:
    pass

apilevel = "2.0"
threadsafety = 0
paramstyle = "named"

logger = logging.getLogger('py4j')


def connect(*args, **kwargs):
    """Constructor for creating a connection to the database.

    See class :py:class:`Connection` for arguments.

    :returns: a :py:class:`Connection` object.
    """
    return Connection(*args, **kwargs)


class Connection:
    """Wraps a spark connect session"""

    def __init__(self,
                 host=DEFAULT_CONNECT_HOST,
                 port=DEFAULT_CONNECT_PORT,
                 token=None,
                 use_ssl=None,
                 user_id=None,
                 user_agent=None,
                 session_id=None,
                 grpc_max_message_size=None,
                 config=None):

        self.host = host
        self.port = port
        self.token = token
        self.use_ssl = use_ssl
        self.user_id = user_id
        self.user_agent = user_agent
        self.session_id = session_id
        self.grpc_max_message_size = grpc_max_message_size
        self.config = config
        # TODO: maybe best place to put this?
        self._connect()

    def _connect(self):
        self.spark = SparkSession.getActiveSession()
        if not self.spark:
            if self.config is None:
                self.config = {}
            self.spark = SparkSession.builder.remote(self._create_connection_string()).config(map=self.config).getOrCreate()

    def _create_connection_string(self) -> str:
        """
        https://github.com/apache/spark/blob/master/connector/connect/docs/client-connection-string.md
        :return: sc://host:port/;param1=value;param2=value
        """

        address = str(Url(scheme='sc', host=self.host, port=self.port))
        conn_params = {k: v for k, v in self.__dict__.items() if k in CONN_STRING_PARAMS and v}  # :(
        if conn_params:
            result = address + "/;" + ";".join(f"{k}={v}" for k, v in conn_params.items())
        else:
            result = address
        logging.debug(f"Try create connection with conn string: {address}",)
        # logging.debug("Connecting to %s", address)
        return result

    def __enter__(self):
        """Transport should already be opened by __init__"""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Call close"""
        self.close()

    def close(self):
        """Close the underlying session and Thrift transport"""
        session = SparkSession.getActiveSession()
        logging.debug(f"Closing spark session with id: {session.client._session_id}")
        session.client.interrupt_all()
        session.client.close()

        if not session.client.is_closed:
            raise DatabaseError("Spark client not closed")

        logging.debug("Spark session closed")

    def commit(self):
        """does not support transactions, so this does nothing."""
        pass

    def cursor(self, *args, **kwargs):
        """Return a new :py:class:`Cursor` object using the connection."""
        return Cursor(self)

    def rollback(self):
        raise NotSupportedError("Spark does not have transactions")  # pragma: no cover


class Cursor:

    def __init__(self, session: Connection):
        self.connection = session
        self.spark = self.connection.spark #alias
        self._result = None

    def description(self):
        pass

    def execute(self, sql: str, args: Optional[Union[Dict[str, Any], List]] = None):
        if args is not None:
            if isinstance(args, Dict):
                for k, v in args.items():
                    if not isinstance(k, str): raise TypeError(f"Argument '{k}' is not a string")
            else:
                if not isinstance(args, List): raise TypeError(f"Argument '{args}' is not a list")

        self._result = self.spark.sql(sql)
        return self

    def executemany(self):
        NotImplementedError("Not implemented yet")

    def fetchone(self):
        """Returns one result row or None if there are no more rows."""
        if self._result is None:
            raise OperationalError("No executed request. Use the execute() method before fetchone().")
        rows = self._result.collect()
        return tuple(rows[0]) if rows else None

    def fetchall(self):
        """Returns all the results of the query as a list of tuples."""
        if self._result is None:
            raise OperationalError("No executed request. Use the execute() method before fetchall().")
        return [tuple(row) for row in self._result.collect()]

    def fetchmany(self, size=None):
        """Returns the specified number of records of the query results as a list of tuples."""
        if self._result is None:
            raise OperationalError("No executed request. Use the execute() method before fetchmany().")
        return [tuple(row) for row in self._result.collect()][:size]

    def close(self):
        self.connection.close()
