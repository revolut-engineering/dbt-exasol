from __future__ import absolute_import

from dbt.adapters.sql import SQLAdapter
from dbt.adapters.exasol import ExasolConnectionManager
from dbt.adapters.exasol import ExasolRelation
from dbt.logger import GLOBAL_LOGGER as logger
from dbt.utils import filter_null_values
import dbt.flags
from typing import Dict


class ExasolAdapter(SQLAdapter):
    Relation = ExasolRelation
    ConnectionManager = ExasolConnectionManager

    @classmethod
    def date_function(cls):
        return 'current_timestamp()'

    @classmethod
    def is_cancelable(cls):
        return False

    @classmethod
    def convert_text_type(cls, agate_table, col_idx):
        column = agate_table.columns[col_idx]
        lens = (len(d.encode("utf-8")) for d in column.values_without_nulls())
        max_len = max(lens) if lens else 64
        return "varchar({})".format(max_len)

    def _make_match_kwargs(
        self, database: str, schema: str, identifier: str
    ) -> Dict[str, str]:
        quoting = self.config.quoting
        if identifier is not None and quoting['identifier'] is False:
            identifier = identifier.lower()

        if schema is not None and quoting['schema'] is False:
            schema = schema.lower()

        if database is not None and quoting['database'] is False:
            database = database.lower()

        return filter_null_values({
            'identifier': identifier,
            'schema': schema,
        })