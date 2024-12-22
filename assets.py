import sqlite3 as sq
import secrets as st


class Database:
    def __init__(self):
        self.connection = sq.connect("urls.db")

    def add_key(self, url):
        cursor = self.connection.cursor()
        key = self.create_key()
        cursor.execute("INSERT INTO Keys VALUES (?,?)",(key, url))
        self.connection.commit()
        self.connection.close()
        return key

    @staticmethod
    def create_key():
        key = st.token_urlsafe(12)
        return key

    def get_url(self, key):
        cursor = self.connection.cursor()
        cursor.execute("SELECT url FROM Keys WHERE Key=?",(key,))
        x = cursor.fetchone()
        self.connection.close()
        if x:
            return x[0]
        else:
            return None
