import socket,string
host=socket.gethostbyname(socket.gethostname())

if host.startswith('192.168'):
    host='localhost'
else:
    host='other'

if host == 'localhost':
    path_to_repo=''
else :
    path_to_repo='/home/vgoel38/EmpowerK-12/'