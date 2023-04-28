import sqlite3
from typing import List, Any, Tuple, Union


class SQLite():
    def __init__(self, file='sql.db'):
        self.file = file

    def __enter__(self):
        self.conn = sqlite3.connect(self.file)
        self.conn.row_factory = sqlite3.Row
        return self.conn.cursor()

    def __exit__(self, type, value, traceback):
        self.conn.commit()
        self.conn.close()


def execute_sql(sql: str, variables: Union[Tuple, List] = None):
    with SQLite('sql.db') as cur:
        try:
            if variables:
                return cur.execute(sql, variables).fetchall()
            return cur.execute(sql).fetchall()
        except sqlite3.Error as error:
            print('Error occurred - ', error)
            raise error
