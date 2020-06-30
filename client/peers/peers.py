import requests
import json

class Peers:
  def getPeers(tracker_ip, info_hash, ip, port, event, peer_id):
    payload = {'info_hash': info_hash, 'ip': ip, 'port': port, 'event': event, 'peer_id': peer_id}
    answer = requests.get(tracker_ip, params=payload)
    return answer.json()