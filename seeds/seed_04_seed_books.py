from datetime import datetime, date, timedelta

from helpers import random_date
from objects.books import BookManager

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
        manager = BookManager()
        for title, info in SEED_DATA.items():
            try:
                author = info["author"]
                isbn = info["isbn"]
                now = date.today()
                publish_date = random_date(now - timedelta(days=365), now)
                book = manager.get_isbn(isbn)
                if book:
                    continue
                result = manager.create(title=title, author=author, isbn=isbn, publish_date=publish_date)
                print(result)
            except Exception as ex:
                print(ex)


if __name__ == "__main__":
    Migration().migrate()
