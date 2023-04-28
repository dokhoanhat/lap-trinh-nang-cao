from datetime import datetime
from functools import cached_property, partial
from typing import List, Union

from helpers import define_field_type
from objects.cores import BaseManager, OOPObject
from objects.wrappers import execute_sql


class Account(OOPObject):
    id: define_field_type(int, primary_key=True, auto_increment=True)
    username: define_field_type(str, unique=True)
    password: define_field_type(str)
    name: define_field_type(str)
    is_active: define_field_type(bool, default=True)
    created: define_field_type(datetime, default=datetime.now)
    table_name = "Account"
    fields = [
        "id",
        "username",
        "password",
        "name",
        "is_active",
        "created",
    ]
    from objects.books import Book, Borrow

    @cached_property
    def my_borrows(self, **kwargs):
        from objects.books import BorrowManager
        return BorrowManager().filter(account_id=self.id, **kwargs)

    def borrow(self, book: Union[Book, int]):
        from objects.books import Book, BorrowManager
        book_id = book.id if isinstance(book, Book) else book
        return BorrowManager().create(account_id=self.id, book_id=book_id)

    def return_book(self, borrow: Union[Borrow, int]):
        from objects.books import Borrow, BorrowManager
        borrow_id = borrow.id if isinstance(borrow, Borrow) else borrow
        borrow_instance = BorrowManager().filter(id=borrow_id, account_id=self.id)[0]
        borrow_instance.return_date = datetime.now()
        borrow_instance.save()
        return borrow_instance


class AccountManager(BaseManager):
    object_class = Account
    search_fields = [
        "username",
        "name",
    ]

    def authenticate(self, username: str, password: str):
        sql = f"""
        SELECT * FROM {self.object_class.table_name}
        WHERE username = ? and password = ?;
        """
        results = execute_sql(sql, [username, password])
        if not results:
            return
        return self.init(*[item for item in results[0]])


class Librarian(OOPObject):
    id: define_field_type(int, primary_key=True, auto_increment=True)
    account_id: define_field_type(int, foreign_key=Account, unique=True)
    table_name = "Librarian"
    fields = [
        "id",
        "account_id",
    ]


class LibrarianManager(BaseManager):
    object_class = Librarian

    def authenticate(self, username: str, password: str):
        sql = f"""
        SELECT * FROM {self.object_class.table_name}
        INNER JOIN Account on {self.object_class.table_name}.id = Account.id
        WHERE Account.username = ? and Account.password = ?;
        """
        results = execute_sql(sql, [username, password])
        if not results:
            return
        return self.init(*[item for item in results[0]])
