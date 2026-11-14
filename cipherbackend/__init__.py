import pymysql
from django.db.backends.base.base import BaseDatabaseWrapper
from django.db.backends.mysql.features import DatabaseFeatures
from django.db.backends.mysql.schema import DatabaseSchemaEditor

pymysql.install_as_MySQLdb()

# Bypass MariaDB version check for older XAMPP MariaDB versions
BaseDatabaseWrapper.check_database_version_supported = lambda self: None

# MariaDB < 10.5 does not support INSERT ... RETURNING syntax
DatabaseFeatures.can_return_columns_from_insert = property(
    lambda self: bool(self.connection.mysql_is_mariadb and self.connection.mysql_version >= (10, 5))
)

# MariaDB < 10.5.2 does not support ALTER TABLE ... RENAME COLUMN syntax (use CHANGE instead)
_orig_rename_field_sql = DatabaseSchemaEditor._rename_field_sql

def _custom_rename_field_sql(self, table, old_field, new_field, new_type):
    if self.connection.mysql_is_mariadb and self.connection.mysql_version < (10, 5, 2):
        new_type = self._set_field_new_type(old_field, new_type)
        return "ALTER TABLE %(table)s CHANGE %(old_column)s %(new_column)s %(type)s" % {
            "table": self.quote_name(table),
            "old_column": self.quote_name(old_field.column),
            "new_column": self.quote_name(new_field.column),
            "type": new_type,
        }
    return _orig_rename_field_sql(self, table, old_field, new_field, new_type)

DatabaseSchemaEditor._rename_field_sql = _custom_rename_field_sql
