import socket
import struct
from threading import Thread
from client.file.messages import Messages
from client.file.read_file import ReadFile
import sys
sys.path.append("..")
from client.db.file_table import FileTable

BUFFER_SIZE = 1024

class SendThread(Thread):
  def __init__(self, connection):
    self.connection = connection


  def run(self):

    # First message needs to be the handshake
    data = self.connection.recv(BUFFER_SIZE)
    print(data)
    data = data.decode("utf-8")
    print(data)
    self.connection.send(b"ok")
    info_hash = Messages.getInfoHash(data)
    print(info_hash)
    path = FileTable.getByInfoHash(info_hash)
    print(path)
    file = open(path, "r")
    while True:
      data = self.connection.recv(BUFFER_SIZE)
      data = data.decode("utf-8")
      mt = int(Messages.getMessageType(data))
      if(mt == 1):
        pieceNumber = int(Messages.getNPiece(data))
        piece = ReadFile.getNPiece(file, pieceNumber, 65536)
        print(piece)
        self.connection.send(piece.encode())
      if(mt == 2):
        break
    file.close()
    self.connection.send(b"finished")
    self.connection.close()

TCP_IP = '127.0.0.1'
TCP_PORT = 5050
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((TCP_IP, TCP_PORT))
s.listen(3)

while True:
  conn, addr = s.accept()
  st = SendThread(conn)
  st.run()