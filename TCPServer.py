'''
TCP Multi-threaded socket program. Multi-threading is needed in order
to allow to processes or threads to execute. Each client established
is it's own "thread" which is executed by the server. Without threading execution would happen sequentially. Ideally processing would be done in parrallel so
server resources are not wasted, and other users do not have to wait'''



import socket
import threading
import json

class Server():
	hostname = ''
	port = 0
	socket = None
	clients = []
	dead = False
	__thread = None				# Receiving messages
	__connectionThread = None	# Listening for connections
	

	def __init__(self, hostname, port):
		self.hostname = hostname
		self.port = port

		self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) # Fixes socket use

		self.socket.bind((hostname, port))
		self.socket.listen(2) 						
		self.socket.setblocking(False)

		self.__connectionThread = threading.Thread(target = self.accept) # Listening for connections
		self.__connectionThread.start()

		self.__thread = threading.Thread(target = self.receive)
		self.__thread.start()
		self.tempMessages = []

	def shutdown(self):
		self.socket.close()
		self.dead = True

	def accept(self):
		while not self.dead:
			try:
				connection, address = self.socket.accept()

				self.clients.append((connection, address))
			except: 
				pass


	def receive(self):
		while not self.dead:
			
			for client, address in self.clients:
				#try:
					if(len(self.clients) == 2):
						packet = client.recv(2048)

						data = json.loads(packet.decode()) # Reloaded from json
					
						self.tempMessages.append(data)
						self.onMessageReceived(client, address, data)

						if len(self.tempMessages) == 2: # After the first 2 messages, print out the order they came in
							if self.tempMessages[0]["timestamp"] < self.tempMessages[1]["timestamp"]:
								order = str(self.tempMessages[0]["username"] + ": " + self.tempMessages[0]["message"] + " " + "received before" + " " + self.tempMessages[1]["username"] + ": " + self.tempMessages[1]["message"])
							else:
								order = str(self.tempMessages[1]["username"] + ": " + self.tempMessages[1]["message"] + " " + "received before" + " " + self.tempMessages[0]["username"] + ": " + self.tempMessages[0]["message"])
						
							order1 = json.dumps(order)
							encoded = order1.encode()
							for client,address in self.clients:	# Send the order string back to all the clients
								client.sendall(encoded)
							print(order)
							self.shutdown()
				#except:
				#	pass


	def onMessageReceived(self, client, address, message):
		while 1:	
			if(len(self.clients) == 2):
				print(message["username"] + ":", message["message"])
				break


#execute server 
if __name__ == "__main__":
    print('The server is ready to receive')
    server = Server('localhost', 1200)


