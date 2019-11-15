import socket 
import json
import threading 
import time

class Client():
    destination = ""
    port = 0
    dead = False
    socket = None
    username = ""
    __thread = None
    __inputThread = None

    def __init__(self, username):
        self.username = username    # Initalize username

    def connect(self, ip, port):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # Opening sockets
        self.socket.connect((ip, port))
        self.socket.setblocking(False)

        self.__thread = threading.Thread(target = self.receive)  # Creates new thread, while true loop
        self.__thread.start()

        self.__inputThread = threading.Thread(target = self.run)
        self.__inputThread.start()

    def disconect(self):
        self.socket.close()
        self.dead = True # Closing thread

    def run(self): #Input for message
        while not self.dead:
            text = input("Client " + self.username + ": ") #Indicating typing
            self.sendMessage(text) #Sending the message

    def sendMessage(self, message):
        packet = {'username': self.username, 'message': message, 'timestamp' : time.time()} # Inserting user and message

        packed = json.dumps(packet)

        encoded = packed.encode()
        
        self.socket.sendall(encoded)    #Sendall sends everything to the server

    def receive(self):
        while not self.dead:
            try:
                packet = self.socket.recv(2048)
                
                if(not packet):
                    continue
                
                data = json.loads(packet.decode())
                
                self.onMessageReceived(data)
         
            except:
                pass

    def onMessageReceived(self, message):
       	print(message)
      
