import sqlite3
import os.path

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

class Peers:
  def __init__(self, ip, port):
    self.ip = ip
    self.port = port

class PeersTable:
  def __init__():
    pass

  def insert(info_hash, peer_id, ip, port, event):
    conn = sqlite3.connect(BASE_DIR + '/info.db')
    c = conn.cursor()
    data = (info_hash, peer_id, ip, port, event)
    c.execute("INSERT INTO peers VALUES (?, ?, ?, ?, ?)", data)
    conn.commit()
    conn.close()

  def getByInfoHash(info_hash):
    conn = sqlite3.connect(BASE_DIR + '/info.db')
    c = conn.cursor()
    c.execute('SELECT ip, port FROM peers WHERE info_hash=? AND event != 2', (info_hash,))
    
    peers = []
    row = c.fetchone()
    while(row != None):
      peers.append(Peers(row[0], row[1]))
      row = c.fetchone()

    conn.close()
    return peers      
