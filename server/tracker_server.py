from flask import Flask, request, jsonify
from flask_restful import Resource, Api
from json import dumps
from db.peers_table import PeersTable

app = Flask(__name__)
api = Api(app)

class Announce(Resource):
  def get(self):
    info_hash = request.args.get('info_hash')
    peer_id = request.args.get('peer_id')
    ip = request.args.get('ip')
    port = request.args.get('port')
    event = request.args.get('event')

    peers = PeersTable.getByInfoHash(info_hash)
    PeersTable.insert(info_hash, peer_id, ip, port, event)

    response = jsonify([o.__dict__ for o in peers])   
    return response

api.add_resource(Announce, '/announce')

if __name__ == '__main__':
  app.run(debug=True)