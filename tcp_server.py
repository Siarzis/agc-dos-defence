import socket

HOST = '127.0.0.1'
PORT = 65432

# 'with' statement handles exceptions, opening/closing sockets, etc.
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    
    s.listen()
    print('Server is working! Waiting for connections...')

    conn, addr = s.accept()

    with conn:
        print('Successful connection from ', addr)
        while True:
            