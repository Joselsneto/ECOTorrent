import socket
TCP_IP = '127.0.0.1'
TCP_PORT = 5005
BUFFER_SIZE = 65536 
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((TCP_IP, TCP_PORT))
s.send(b"146EcoTorrent00000000cb9266b9244d6aab3adad9039fc5d8414de20b503c701a7b64bf60610b5ff755-ET0001-1f99441bc819ff607664031b92696811bd50cd81468fbe56b931c4e7")
data = s.recv(BUFFER_SIZE)
print( "received data:", data)
s.send(b"00010")
data = s.recv(BUFFER_SIZE)
print("data: ", data)
s.send(b"00011")
data = s.recv(BUFFER_SIZE)
print("data: ", data) 
s.send(b"0002")
data = s.recv(BUFFER_SIZE)
print("f:", data)
s.close()