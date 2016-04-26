import socket,string
host=socket.gethostbyname(socket.gethostname())

#10.0.2.15 is my vagrant private ip address and 192.168.1.10 is my private ip address
if host.startswith('192.168') or host.startswith('10.0.2.15'):
    host='localhost'
else:
    host='other'

if host == 'localhost':
    path_to_repo=''
else :
    path_to_repo='/home/vgoel38/EmpowerK-12/'