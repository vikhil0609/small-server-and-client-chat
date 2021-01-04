import time
from threading import Thread
import socket


HOST = socket.gethostbyname(socket.gethostname())
PORT = 5000
ADDR = (HOST,PORT)
BUFSIZ = 1024
MAX_CONNECTIONS = 10
class Client:
	def __init__(self):
		self.client_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
		self.client_socket.connect(ADDR)
		reveive_thread = Thread(target = self.receive_messages)
		reveive_thread.start()


	def receive_messages(self):

		while True:
			try:
				msg = self.client_socket.recv(BUFSIZ).decode('utf8')
				if msg.lower() == "quit":
					self.terminting_socket()
				else:
					print(msg)
					return msg
			except Exception as e:
				terminting_socket()

	def send_messages(self,msg):
		time.sleep(2)
		self.client_socket.send(bytes("client:"+str(msg),'utf8'))


	def terminting_socket(self):
		print("communication gateway closed")
		self.client_socket.close()
