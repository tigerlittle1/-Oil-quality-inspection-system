import socket

class Client():
    def __init__(self,ip = '0.tcp.ngrok.io',port = 19446):
        self.HOST = ip
        self.PORT = port
        self.client = None

    def init_connect(self,ip = '0.tcp.ngrok.io',port = 19446):
        self.HOST = ip
        self.PORT = port
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.client.connect((self.HOST, self.PORT))
        except socket.timeout:
            print("test")
            return False

    def sned_message(self,message):
        self.client.sendall(message.encode())

    def get_message(self):
        serverMessage = str(self.client.recv(1024), encoding='utf-8')
        return serverMessage

    def close_connet(self):
        if self.client != None:
            print("close")
            self.client.close()
            self.client = None