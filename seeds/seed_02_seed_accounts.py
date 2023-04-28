from objects.users import AccountManager
import random

SEED_DATA = {
    "admin": "admin",
    "a": "1",
    "b": "2",
    "c": "3",
}

FIRST_NAMES = [
    "James",
    "Alice",
    "Bob",
    "Trent",
    "Jack",
]

LAST_NAMES = [
    "Copper",
    "Smith",
    "Anderson",
    "Reeves",
]


class Migration():
    def migrate(self):
        manager = AccountManager()
        for username, password in SEED_DATA.items():
            try:
                existing_accounts = manager.filter(username=username)
                if existing_accounts:
                    continue
                result = manager.create(username=username, password=password, name=self.get_random_name())
                print(result)
            except Exception as ex:
                print(ex)

    def get_random_name(self):
        return f"{random.choice(FIRST_NAMES)} {random.choice(LAST_NAMES)}"


if __name__ == "__main__":
    Migration().migrate()
