import os
from flask import Flask
from objects.wrappers import execute_sql
from routers.admin import admin_page
from routers.urls import main_page

execute_sql("CREATE TABLE IF NOT EXISTS INIT (id tinyint)")
init_records = execute_sql("SELECT * FROM INIT")
if not init_records:
    print("Running seeds")
    from seeds.seed_01_init import Migration as migration_01
    from seeds.seed_02_seed_accounts import Migration as migration_02
    from seeds.seed_03_seed_librarians import Migration as migration_03
    from seeds.seed_04_seed_books import Migration as migration_04
    from seeds.seed_05_seed_borrows import Migration as migration_05
    migration_01().migrate()
    migration_02().migrate()
    migration_03().migrate()
    migration_04().migrate()
    migration_05().migrate()
    execute_sql("INSERT INTO INIT (id) VALUES (0)")


app = Flask(__name__)
app.register_blueprint(main_page)
app.register_blueprint(admin_page)
app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'


