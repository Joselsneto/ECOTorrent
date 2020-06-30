import argparse
import hashlib
import os
import sys
import json
from client.file.ecotorrent_file import EcotorrentFile

sys.path.append("..")
from client.db.file_table import FileTable

DEFAULT_PIECE_LENGTH = 65536


def create_file(output_file, infos):
    try:
        file = open(output_file, "w")
        file.write(infos)
        file.close()
    except Exception as e:
        raise e


def get_file_info(ip, file_path, private, piece_length, pieces):
    baseName = os.path.basename(file_path)
    size = os.path.getsize(file_path)

    ecot = EcotorrentFile(ip, piece_length, private, pieces, baseName, size)
    file_info = ecot.toEcot()
    return file_info


def read_file(file_path, piece_length):
    try:
        file = open(file_path, 'rb')
        str_hash = ""

        while True:
            piece = file.read(piece_length)
            if not piece:
                break
            m = hashlib.sha256()
            m.update(piece)
            str_hash = "{}{}".format(str_hash, m.hexdigest())
        file.close()

        return str_hash

    except Exception as e:
        raise e


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("file_path", type=str, help="The file that you want to create.")
    parser.add_argument("-ip", "--tracker_ip", type=str, help="The tracker ip that you want to connect.")
    parser.add_argument("-p", "--private", type=bool, help="If the tracker use a private IP, default = false")
    parser.add_argument("-pl", "--piece_length", type=int,
                        help="Piece length in bytes, it's recommended to use size of 2^n, default = 65536.")
    parser.add_argument("output_file", type=str, help="The name of the output file.")

    args = parser.parse_args()

    file_path = args.file_path
    ip = args.tracker_ip
    private = (args.private if args.private != None else False)
    piece_length = (args.piece_length if args.piece_length != None else DEFAULT_PIECE_LENGTH)
    output_file = args.output_file

    str_hash = read_file(file_path, piece_length)
    infos = get_file_info(ip, file_path, private, piece_length, str_hash)
    hash_info = hashlib.sha256(infos.encode('utf-8')).hexdigest()
    print(hash_info)
    f_name = os.path.basename(file_path)
    f_size = json.loads(infos)['info']['length']
    FileTable.insert(hash_info, file_path, f_name, f_size)
    create_file(output_file, infos)
