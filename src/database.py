""" A module for the persistence layer """

import sqlite3
import typing as t

from textwrap import dedent


class DatabaseManager:
    """A class specialized for the persistence layer using SQLite"""

    def __init__(self, database_filename: str):
        """Initializes the connection with the SQLite database"""

        self.connection = sqlite3.connect(database_filename)

    def __del__(self):
        """Closes the connection when the database manager is no longer used"""

        self.connection.close()

    def _execute(
        self, statement: str, values: t.Optional[t.Tuple[t.Union[str, int], ...]] = None
    ) -> sqlite3.Cursor:
        """
        Takes in a SQL statement and optionally the values for placeholders
        and executes it with SQLite
        """
        try:
            with self.connection:
                cursor = self.connection.cursor()
                cursor.execute(statement, values or [])
                return cursor
        except (sqlite3.IntegrityError, sqlite3.OperationalError):
            print(f"Something went wrong with the following transaction:\n{statement}")
            raise

    def create_table(self, table_name: str, columns: t.Dict[str, str]) -> None:
        """
        Takes in a table name and the columns with names as keys and types as values and creates
        the CREATE TABLE statement to be executed with SQLite
        """
        columns_with_types = []

        for column_name, data_type in columns.items():
            current_column = f"{column_name} {data_type.upper()}"
            columns_with_types.append(current_column)

        columns_in_statement = ", ".join(columns_with_types)

        statement = dedent(
            f"""
                CREATE TABLE IF NOT EXISTS {table_name} (
                    {columns_in_statement}
                );
            """
        )

        self._execute(statement)

    def drop_table(self, table_name: str) -> None:
        """
        Takes in a table name to delete using the DROP TABLE statement to be executed with SQLite
        """

        statement = f"DROP TABLE {table_name};"
        self._execute(statement)

    def add(self, table_name: str, data: t.Dict[str, str]) -> None:
        """
        Takes in a table name to INSERT data INTO and a data dictionary with columns
        as keys and values as values
        """

        column_names = ", ".join(data.keys())
        placeholders = ", ".join(["?"] * len(data.keys()))
        column_values = tuple(data.values())

        statement = dedent(
            f"""
            INSERT INTO
                {table_name} (
                    {column_names}
                ) VALUES (
                    {placeholders}
                );
            """
        )

        self._execute(statement, column_values)

    def delete(self, table_name: str, criteria: t.Dict[str, t.Union[str, int]]) -> None:
        """
        Takes in a table name and a criteria to DELETE FROM
        """

        placeholders = [f"{column} = ?" for column in criteria.keys()]
        delete_criteria = " AND ".join(placeholders)
        delete_criteria_values = tuple(criteria.values())

        statement = dedent(
            f"""
                DELETE FROM
                    {table_name}
                WHERE
                    {delete_criteria};
            """
        )

        self._execute(statement, delete_criteria_values)

    def select(
        self,
        table_name: str,
        criteria: t.Dict[str, str] = {},
        order_by: t.Optional[str] = None,
        ordered_descending: bool = False,
    ) -> sqlite3.Cursor:
        """
        Takes in a table name and optionally a criteria as a dictionary, a column to order by
        and a boolean flag to order it by that column descending or not
        """

        select_criteria_values = tuple(criteria.values())

        statement = f"SELECT * FROM {table_name}"
        if criteria:
            placeholders = [f"{column} = ?" for column in criteria.keys()]
            select_criteria = " AND ".join(placeholders)
            statement = statement + f" WHERE {select_criteria}"

        if order_by:
            statement = statement + f" ORDER BY {order_by}"
            if ordered_descending:
                statement = statement + " DESC"

        statement = statement + ";"

        return self._execute(statement, select_criteria_values)

    def update(
        self,
        table_name: str,
        criteria: t.Dict[str, str] = {},
        data: t.Dict[str, str] = {},
    ):
        placeholders = [f"{column} = ?" for column in criteria.keys()]
        update_criteria = " AND ".join(placeholders)

        data_placeholders = ", ".join([f"{key} = ?" for key in data.keys()])
        values = tuple(data.values()) + tuple(criteria.values())

        statement = (
            f"UPDATE {table_name} SET {data_placeholders} WHERE {update_criteria};"
        )

        self._execute(statement, values)
