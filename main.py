from client import Client
from threading import Thread , Lock
import time

def updated_messages():
	try:
		while True:
			messages = c1.receive_messages()
			if ' ' in messages:
				 answer = input('ENTER YOUR ANSWER:')
				 c1.send_messages(" "+"Answer from client: "+answer)

	except:
		c1.terminting_socket()
input("PRESS ANY KEY TO CONNECT")
c1 = Client()
Thread(target=updated_messages).start()
c1.send_messages('ok')
