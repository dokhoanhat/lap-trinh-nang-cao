from datetime import datetime, date
from functools import cached_property
from typing import List

from helpers import define_field_type
from objects.cores import OOPObject, BaseManager
from objects.wrappers import execute_sql


class Book(OOPObject):
    id: define_field_type(int, primary_key=True, auto_increment=True)
    title: define_field_type(str)
    author: define_field_type(str)
    isbn: define_field_type(str)
    publish_date: define_field_type(date)
    created: define_field_type(datetime, default=datetime.now)
    table_name = "Book"
    fields = [
        "id",
        "title",
        "author",
        "isbn",
        "publish_date",
        "created",
    ]

    @cached_property
    def borrowers(self):
        return

    @cached_property
    def borrows(self):
        return


class BookManager(BaseManager):
    object_class = Book
    search_fields = [
        "title",
        "author",
        "isbn",
    ]

    def get_isbn(self, isbn: str):
        sql = f"""
        SELECT * FROM {self.object_class.table_name}
        WHERE isbn = ?;
        """
        results = execute_sql(sql, [isbn])
        if not results:
            return
        return self.init(*[item for item in results[0]])


class Borrow(OOPObject):
    id: define_field_type(int, primary_key=True, auto_increment=True)
    account_id: define_field_type(str)
    book_id: define_field_type(str)
    borrow_time: define_field_type(datetime, default=datetime.now)
    return_time: define_field_type(datetime)
    table_name = "Borrow"
    fields = [
        "id",
        "account_id",
        "book_id",
        "borrow_time",
        "return_time",
    ]

    @property
    def account(self):
        from objects.users import AccountManager
        return AccountManager().get(self.account_id)

    @property
    def book(self):
        return BookManager().get(self.book_id)


class BorrowManager(BaseManager):
    object_class = Borrow
    search_fields = [
        "account.username",
        "account.name",
        "book.title",
        "book.isbn",
    ]

    def search(self, search: str, ordering: List[str] = None, **kwargs):
        sql = f"""
        SELECT * FROM {self.object_class.table_name}
        INNER JOIN account on {self.object_class.table_name}.account_id = account.id
        INNER JOIN book on {self.object_class.table_name}.book_id = book.id
        """
        if self.search_fields:
            sql += f" {self.handle_search_conditions(**kwargs)}"
        if ordering:
            sql += f" {self.handle_ordering(ordering)}"

        pattern = f"%{search.lower()}%"
        variables = list(kwargs.values()) + ([pattern]*len(self.search_fields))
        results = execute_sql(sql, variables)
        if not results:
            return []
        values_list = [[item for item in result] for result in results]
        return self.init_list(values_list)
