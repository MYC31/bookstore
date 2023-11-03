import logging
import os
import sqlite3 as sqlite


class Store:
    database: str

    def __init__(self, db_path):
        self.database = os.path.join(db_path, "be.db")
        self.init_tables()

    def init_tables(self):
        try:
            conn = self.get_db_conn()
            conn.execute(
                "CREATE TABLE IF NOT EXISTS user ("
                "user_id TEXT PRIMARY KEY, password TEXT NOT NULL, "
                "balance INTEGER NOT NULL, token TEXT, terminal TEXT);"
            )

            conn.execute(
                "CREATE TABLE IF NOT EXISTS user_store("
                "user_id TEXT, store_id, PRIMARY KEY(user_id, store_id));"
            )

            conn.execute(
                "CREATE TABLE IF NOT EXISTS store( "
                "store_id TEXT, book_id TEXT, book_info TEXT, stock_level INTEGER,"
                " PRIMARY KEY(store_id, book_id))"
            )

            conn.execute(
                "CREATE TABLE IF NOT EXISTS new_order( "
                "order_id TEXT PRIMARY KEY, user_id TEXT, store_id TEXT)"
            )

            conn.execute(
                "CREATE TABLE IF NOT EXISTS new_order_detail( "
                "order_id TEXT, book_id TEXT, count INTEGER, price INTEGER,  "
                "PRIMARY KEY(order_id, book_id))"
            )

            # conn.execute(
            #     "CREATE TABLE IF NOT EXISTS book( "
            #     "id TEXT, title TEXT, author TEXT, publisher TEXT, original_title TEXT, translator TEXT, pub_year TEXT, pages INTEGER, "
            #     "price INTEGER, currency_unit TEXT, binding TEXT, isbn TEXT, author_intro TEXT, book_intro TEXT, "
            #     "content TEXT, tags TEXT, picture TEXT, "
            #     "PRIMARY KEY(id))"
            # )

            conn.commit()
        except sqlite.Error as e:
            logging.error(e)
            conn.rollback()

    def get_db_conn(self) -> sqlite.Connection:
        return sqlite.connect(self.database)    # establish databse connection suing self.database


# global variable for database instance
database_instance: Store = None


# init function of global variable 
# should be callled before get_db_conn
def init_database(db_path):
    global database_instance
    database_instance = Store(db_path)


# outer plugin for obtaining database instance
# store.get_db_conn
def get_db_conn():
    global database_instance
    # test code of myc
    # print("\n------------")
    # print(f"database_instance: {database_instance}")
    # print("------------\n")
    # test code of myc
    return database_instance.get_db_conn()
