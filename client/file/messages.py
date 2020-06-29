class Messages:
  def __init__(self):
    pass

  def handshake(info_hash, peer_id):
    hs = "146EcoTorrent0000000{}{}".format(info_hash, peer_id)
    return hs

  def verifyHandshake(hs_message):
    pass

  def getInfoHash(hs_message):
    return hs_message[21:85]

  def getMessageType(message):
    return message[0:4]

  def getNPiece(message):
    return message[4:]