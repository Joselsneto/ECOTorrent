import json
import hashlib
import math

class ReadFile:
  def __init__(self):
    pass

  def getInfoHash(file_path):
    with open(file_path) as json_file:
      data = json.load(json_file)
      info = json.dumps(data['info'], sort_keys=True)
      hs = hashlib.sha256(info.encode('utf-8')).hexdigest()
      return hs

  def getTrackerIp(file_path):
    with open(file_path) as json_file:
      data = json.load(json_file)
      trackerIp = data['announce']
      return trackerIp

  def getNPiece(file, n, piece_length):
    file.seek(piece_length*n, 0)
    answer = file.read(piece_length)
    return answer

  def getNHashPiece(file_path, n):
    with open(file_path) as json_file:
      data = json.load(json_file)
      info = data['info']
      pieces = info['pieces']
      return pieces[n*64:(n+1)*64]

  def getNumberOfPieces(file_path):
    with open(file_path) as json_file:
      data = json.load(json_file)
      info = data['info']
      length = int(info['length'])
      piece_length = int(info['piece_length'])
      return math.ceil(length/piece_length)

  def getPieceLength(file_path):
    with open(file_path) as json_file:
      data = json.load(json_file)
      info = data['info']
      length = int(info['length'])
      return length

  def getName(file_path):
    with open(file_path) as json_file:
      info = data['info']
      return info['name']