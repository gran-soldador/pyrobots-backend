from pony.orm import *

db = Database()

db.bind(provider="sqlite", filename="main.db", create_db=True)


class TestMessage(db.Entity):
    msgid = PrimaryKey(int, auto=True)
    text = Required(str, 255)


db.generate_mapping(create_tables=True)
