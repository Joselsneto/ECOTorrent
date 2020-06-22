class EcotorrentFile:
  def __init__(self, announce, piece_length, private, pieces, name, length):
    self.announce = announce
    self.info = Info(piece_length, private, pieces, name, length)

  def toEcot(self):
    info = self.info.toStr()
    answer = "{\"announce\":\"" + self.announce + "\",\"info\":{" + info + "}}"
    return answer


class Info:
  def __init__(self, piece_length, private, pieces, name, length):
    self.piece_length = piece_length
    self.private = 1 if private == True else 0
    self.pieces = pieces
    self.name = name
    self.length = length

  def toStr(self):
    answer = ("\"piece_length\":{},\"private\":{},\"pieces\":\"{}\","
              "\"name\":\"{}\",\"length\":{}"
              ).format(self.piece_length, self.private, self.pieces, self.name, self.length)
    return answer