import json

class ReadConfig:
  def getPeerId(config_path):
    with open(config_path) as json_file:
      data = json.load(json_file)
      peerId = data['peer_id']
      return peerId

  def getPort(config_path):
    with open(config_path) as json_file:
      data = json.load(json_file)
      peerId = data['default_port']
      return peerId