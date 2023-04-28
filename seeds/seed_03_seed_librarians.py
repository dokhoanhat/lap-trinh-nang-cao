from objects.users import AccountManager, LibrarianManager

SEED_DATA = {
    "a": "1",
}


class Migration():
    def migrate(self):
        account_manager = AccountManager()
        lib_manager = LibrarianManager()
        for username, password in SEED_DATA.items():
            try:
                accounts = account_manager.filter(username=username)
                if not accounts:
                    continue
                account = accounts[0]
                librarian = lib_manager.filter(account_id=account.id)
                if librarian:
                    continue
                result = lib_manager.create(account_id=account.id)
                print(result)
            except Exception as ex:
                print(ex)


if __name__ == "__main__":
    Migration().migrate()
