import os
import shutil
from read_file import ReadFile

class ConcatenateFile:
  def concatenateFile(file_path, output_path, temp_folder):
    size = ReadFile.getNumberOfPieces(file_path)
    filenames = []
    for i in range(size):
      piece_hash = ReadFile.getNHashPiece(file_path, i)
      op = "{}/{}".format(temp_folder, piece_hash)
      filenames.append(op)

    with open(output_path, 'wb') as output_file:
      for files in filenames:
        with open(files, 'rb') as f:
          shutil.copyfileobj(f, output_file)