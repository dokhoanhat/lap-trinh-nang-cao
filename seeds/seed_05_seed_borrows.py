import random
from datetime import datetime, timedelta

from helpers import random_date
from objects.books import BookManager, BorrowManager
from objects.users import AccountManager

SEED_DATA = {
    "Book A": {"author": "Author A", "isbn": "0-3805-6542-0"},
    "Book B": {"author": "Author A", "isbn": "0-5306-1480-4"},
    "Book C": {"author": "Author B", "isbn": "0-2885-0007-5"},
    "Book D": {"author": "Author B", "isbn": "0-5505-9316-0"},
    "Book E": {"author": "Author C", "isbn": "0-4583-8232-9"},
    "Book F": {"author": "Author C", "isbn": "0-3781-0222-2"},
}


class Migration():
    def migrate(self):
        manager = BorrowManager()
        book_manager = BookManager()
        account_manager = AccountManager()
        all_accounts = account_manager.filter()
        all_books = book_manager.filter()
        if not all_accounts:
            return
        for book in all_books:
            try:
                account = random.choice(all_accounts)
                now = datetime.now()
                borrow_time = random_date(now - timedelta(days=365), now)
                return_time = random_date(now, now + timedelta(days=365))
                result = manager.create(account_id=account.id, book_id=book.id, borrow_time=borrow_time, return_time=return_time)
                print(result)
            except Exception as ex:
                print(ex)


if __name__ == "__main__":
    Migration().migrate()
