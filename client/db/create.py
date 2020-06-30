import sqlite3
import os.path

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

conn = sqlite3.connect(BASE_DIR + '/files.db')
c = conn.cursor()
c.execute('''CREATE TABLE files (info_hash text, path text, f_name text, f_size text ) ''')
conn.commit()
conn.close()