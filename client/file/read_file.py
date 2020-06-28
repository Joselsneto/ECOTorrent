import json
import hashlib

class ReadFile:
  def __init__(self):
    pass

  def getInfoHash(file_path):
    with open(file_path) as json_file:
      data = json.load(json_file)
      info = json.dumps(data['info'], sort_keys=True)
      hs = hashlib.sha256(info.encode('utf-8')).hexdigest()
      return hs