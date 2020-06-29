import requests

class Peers:
  def getPeers(tracker_ip, info_hash, ip, port, event, peer_id):
    payload = {'info_hash': info_hash, 'ip': ip, 'port': port, 'event': event, 'peer_id': peer_id}
    answer = request.get(tracker_ip, params=payload)
    print(answer.json())