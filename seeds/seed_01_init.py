from typing import List

from objects.books import BookManager, BorrowManager
from objects.cores import BaseManager
from objects.users import AccountManager, LibrarianManager


class Migration():
    def migrate(self):
        object_list: List[BaseManager] = [
            AccountManager(),
            LibrarianManager(),
            BookManager(),
            BorrowManager(),
        ]

        for manager in object_list:
            manager.create_table()


if __name__ == "__main__":
    Migration().migrate()
