from sqlalchemy.dialects import registry
import pytest

registry.register("scsql", "sqlalchemy_scsql.dialect", "SparkConnectorDialect")

pytest.register_assert_rewrite("sqlalchemy.testing.assertions")

from sqlalchemy.testing.plugin.pytestplugin import *
