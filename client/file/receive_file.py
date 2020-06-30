import socket
import argparse
import queue
import os
import hashlib
from messages import Messages
from read_file import ReadFile
from concatenate_file import ConcatenateFile
import sys
sys.path.append("..")
from peers.peers import Peers
from read_config import ReadConfig

CONFIG_PATH = '/home/jose/Projects/unifei/ECOTorrent/client/config.json'

class ReceiveFile:
  def __init__(self, file_path, output_path):
    self.file_path = file_path
    self.output_path = output_path

  def verifyHash(self, data, n):
    piece_hash = ReadFile.getNHashPiece(self.file_path, n)
    m = hashlib.sha256()
    m.update(data)
    return m.hexdigest() == piece_hash

  def saveFile(self, data, n):
    piece_hash = ReadFile.getNHashPiece(self.file_path, n)
    op = "{}/temp/{}".format(os.path.splitext(self.output_path)[0], piece_hash)
    try:
      file = open(op, "w")
      file.write(data)
      file.close()
    except Exception as e:
      raise e

  def getRemainingPieces(self):
    q = queue.Queue()

    op = "{}{}".format(os.path.splitext(self.output_path)[0], "/temp")
    size = ReadFile.getNumberOfPieces(self.file_path)
    if(os.path.isdir(op)):
      for i in range(size):
        piece_hash = ReadFile.getNHashPiece(self.file_path, i)
        aux = "{}/{}".format(op, piece_hash)
        if not os.path.exists(aux):
          q.put(i)
    else:
      os.makedirs(op)
      for i in range(size):
        q.put(i)
    return q

  def start_download(self):
    tracker_ip = "http://{}/announce".format(ReadFile.getTrackerIp(self.file_path))    
    hostname = socket.gethostname()    
    myip = socket.gethostbyname(hostname)    
    peerId = ReadConfig.getPeerId(CONFIG_PATH)    
    info_hash = ReadFile.getInfoHash(self.file_path)
    port = ReadConfig.getPort(CONFIG_PATH)

    peers = Peers.getPeers(tracker_ip, info_hash, myip, port, 0, peerId)

    piece_length = ReadFile.getPieceLength(self.file_path)
    q = self.getRemainingPieces()

    for p in peers:
      if(q.empty()):
        break
      s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
      s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
      s.connect((p['ip'], int(p['port'])))
      handshake = Messages.handshake(info_hash, peerId)
      s.send(handshake.encode())
      data = s.recv(piece_length)
      if(data != b'ok'):
        s.close()
        continue
      cnt = 0
      while not q.empty():
        elem = q.get()
        msg = '0001{}'.format(str(elem))
        s.send(msg.encode())
        data = s.recv(piece_length)
        if(self.verifyHash(data, elem)):
          self.saveFile(data.decode('utf-8'), elem)
          cnt = 0
        else:
          q.put(elem)
          cnt = cnt + 1
        if cnt == 10:
          break
      s.send(b"0002")
      data = s.recv(piece_length)
      s.close()

    temp = "{}{}".format(os.path.splitext(self.output_path)[0], "/temp")
    ConcatenateFile.concatenateFile(self.file_path, self.output_path, temp)

if __name__ == '__main__':
  parser = argparse.ArgumentParser()
  parser.add_argument("file_path", type=str, help="The path to the ecotorrent file")
  parser.add_argument("-op", "--output_path", type=str, help="The path that will be save the file")

  args = parser.parse_args()
  
  file_path = args.file_path
  output_path = args.output_path

  r = ReceiveFile(file_path, output_path)
  r.start_download()
