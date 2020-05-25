import sqlite3
import os.path

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

conn = sqlite3.connect(BASE_DIR + '/info.db')
c = conn.cursor()
c.execute('''CREATE TABLE peers (info_hash text, peer_id text, ip text, port integer, event integer)''')
conn.commit()
conn.close()