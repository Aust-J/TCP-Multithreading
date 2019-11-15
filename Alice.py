from TCPClient import Client #Instantiate new client protocol

alice = Client("X")
alice.connect('localhost', 1200)
#alice.disconnect()
