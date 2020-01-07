import yaml
import socket
from multiprocessing import Process


class Server:
    def __init__(self, name, host, port, weight=1):
        self.name = name
        self.host = host
        self.port = port
        self.weight = weight

    def __str__(self):
        return self.name + " {host:" + self.host + "; port: " + str(self.port) + "; weight: " + str(self.weight) + "}"


class BalanceServer:

    def __init__(self):
        with open('./config.yml') as file:
            config = yaml.load(file, Loader=yaml.FullLoader)

        self.port = config['port']
        self.servers = []

        for item, doc in config['balancers'].items():
            self.servers.append(Server(item, doc['host'], doc['port'], doc['weight'] if 'weight' in doc.keys() else 1))

        print("Using following servers:")
        print(*self.servers, sep="\n")
        print()

        self.current_server = 0
        self.current_counter = -1

        self.listen()

    @staticmethod
    def client_to_server(client_socket, server_socket):
        while True:
            data = client_socket.recv(1024)
            if not data: break
            server_socket.send(data)

    @staticmethod
    def server_to_client(client_socket, server_socket):
        while True:
            data = server_socket.recv(1024)
            if not data: break
            client_socket.send(data)

    def listen(self):
        ssocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        ssocket.bind(('', self.port))
        print("Listening on port", self.port)
        ssocket.listen()

        while True:
            (client_socket, address) = ssocket.accept()
            self.connect_client(client_socket, self.get_next_server())

    def get_next_server(self):
        self.current_counter += 1
        if self.current_counter >= self.servers[self.current_server].weight:
            self.current_counter = 0
            self.current_server += 1
            if self.current_server >= len(self.servers):
                self.current_server = 0

        return self.servers[self.current_server]

    def connect_client(self, csocket, server):
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.connect((server.host, server.port))
        cs = Process(target=BalanceServer.client_to_server, args=(csocket,server_socket))
        sc = Process(target=BalanceServer.server_to_client, args=(csocket,server_socket))
        cs.start()
        sc.start()



if __name__ == '__main__':
    BalanceServer()
