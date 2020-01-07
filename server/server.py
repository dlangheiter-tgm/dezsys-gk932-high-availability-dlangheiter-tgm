import sys
import socket
from multiprocessing import Process


class Server:
    def __init__(self, name, port):
        self.name = name
        self.port = port

        ssocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        ssocket.bind(('', port))
        print("Server", name, "listening on port", port)
        ssocket.listen()

        while True:
            (client_socket, address) = ssocket.accept()
            p = Process(target=self.client, args=(client_socket,))
            p.start()

    def client(self, client):
        client.send(("Connected to server " + self.name + "\n").encode(),)
        while True:
            data = client.recv(1024)
            if not data: break
            send = "ECHO: " + data.decode('utf-8')
            client.send(send.encode())


if __name__ == '__main__':
    if len(sys.argv) < 3:
        print("Usage: python server.py <name> <port>")
        sys.exit(1)

    name = sys.argv[1]
    port = int(sys.argv[2])
    Server(name, port)
