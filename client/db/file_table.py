import sqlite3
import os.path

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

class FileTable:
  def __init__():
    pass

  def insert(info_hash, path, f_name, f_size):
    conn = sqlite3.connect(BASE_DIR + '/files.db')
    c = conn.cursor()
    data = (info_hash, path, f_name, f_size)
    c.execute("INSERT INTO files VALUES (?, ?, ?, ?)", data)
    conn.commit()
    conn.close()

  def getByInfoHash(info_hash):
    conn = sqlite3.connect(BASE_DIR + '/files.db')
    c = conn.cursor()
    try:
      c.execute('SELECT path FROM files WHERE info_hash=?', (info_hash,))
      row = c.fetchone() 
      path = row[0]
    except Exception as e:
      path = None
    finally: 
      conn.close()
    return path