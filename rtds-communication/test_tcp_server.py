import socket

# TODO: IP, PORT variables must be included in a config file
IP = '127.0.0.1'
PORT = 65432

# 'with' statement handles exceptions, opening/closing sockets, etc.

# socket.AF_INET specify  the Internet address family for IPv4
# socket.SOCK_STREAM specify the socket type for TCP 

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((IP, PORT))
    
    s.listen()
    print('Server is working! Waiting for connections...')

    # socket blocks on accept() method
    conn, addr = s.accept()

    with conn:
        print('Successful connection from', addr)
        while True:
            data = conn.recv(1024)
            if not data:
                break
            else:
                print(addr, 'says :', data)
            conn.sendall(data)