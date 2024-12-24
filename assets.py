import sqlite3 as sq
import secrets as st
import pyqrcode as pc
from io import BytesIO
import base64

class Database:
    def __init__(self):
        self.connection = sq.connect("urls.db")

    def add_key(self, url):
        cursor = self.connection.cursor()
        key = self.create_key()
        if self.check_url(url):
            cursor.execute("SELECT key,qr FROM Keys WHERE url=?", (url,))
            key = cursor.fetchone()
            return key[0], key[1]
        else:
            qr = self.generate_qr(f"https://maskurl.pythonanywhere.com/{key}")
            cursor.execute("INSERT INTO Keys VALUES (?,?,?)", (key, url, qr))
            self.connection.commit()
            self.connection.close()
            return key, qr

    def check_url(self, url):
        cursor = self.connection.cursor()
        cursor.execute("SELECT url FROM Keys")
        urls = cursor.fetchall()
        urls = [i[0] for i in urls]
        return url in urls

    @staticmethod
    def create_key():
        key = st.token_urlsafe(12)
        return key

    @staticmethod
    def generate_qr(link):
        if not link.startswith("http"):
            link = "https://" + link
        qr = pc.create(link)
        buffer = BytesIO()
        qr.png(buffer, scale=10)
        buffer.seek(0)
        qr_data = base64.b64encode(buffer.getvalue()).decode()
        return qr_data

    def get_url(self, key):
        cursor = self.connection.cursor()
        cursor.execute("SELECT url FROM Keys WHERE Key=?",(key,))
        x = cursor.fetchone()
        self.connection.close()
        if x:
            return x[0]
        else:
            return None


