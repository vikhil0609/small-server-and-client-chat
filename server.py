import socket
from threading import Thread
from person import Person
import random
import time
import datetime


HOST = socket.gethostbyname(socket.gethostname())
PORT = 5050
ADDR = (HOST,PORT)
BUFSIZ = 1024
MAX_CONNECTIONS = 2
SERVER = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
SERVER.bind(ADDR)


#LIST OF NAMES JOINED PERSONS
Persons = []
operations = {"add":'+',"sub":'-',"mul":'*',"div":'//',"fadd":'+',"fsub":'-',"fmul":'*',"fdiv":'/'}


def broadcast(msg):
	if msg.find("Answer") > 1:
		x = msg.split(" ")
		for y in x:
			if y.isdigit():
				if int(answer) == int(y):
					print("RIGHT")
				else:
					print("WRONG")
					broadcast("quit")
	else:
		try:
			for person in Persons:
				client = person.client
				time.sleep(2)
				client.send(bytes(msg, 'utf8'))
		except Exception as e:
			print('[3:EXCEPTION]',e)


def evaluate(num1 , num2 , command):
	global answer
	for key , value in operations.items():
		if command == key:
			answer = eval(f"num1 {value} num2")
			print("ANSWER AFTER EVALUATION",answer)


def client_communication(person):
	client = person.client
	run = True
	try:
		while run:
			msg = client.recv(BUFSIZ).decode('utf8')
			print(msg)
			broadcast(msg)
			if msg.lower() == 'quit':
				Persons.remove(person)
				print("client has left the chat")

			else:
				command = random.choice(list(operations.keys()))
				if command == "fadd" or command == "fsub" or command == "fmul" or command == "fdiv":
					num1 = random.uniform(1,100)
					num2 = random.uniform(1,100)
				else:
					num1 = random.randint(1,100)
					num2 = random.randint(1,100)

				print(str(num1) + ' ' + command +' '+ str(num2))
				broadcast(str(num1) + ' ' + command +' '+ str(num2))
				evaluate(num1,num2,command)
	except Exception as e:
			run = False
			Persons.remove(person)
			print("client has left the chat")
			client.close()


def wait_for_communication(SERVER):
	global person
	run = True
	while run:
		try:
			client , addr = SERVER.accept()
			person = Person(addr  , client)
			Persons.append(person)
			print(f"[CONNECTION] from {addr} at {datetime.datetime.now()}")
			message = "TEXT TCP 1.0"
			broadcast("SERVER:"+message)
			Thread(target=client_communication,args=(person,)).start()

		except Exception as e:
			print('[1:EXCEPTION]',e)
			client.close()
	print('[SERVER CRASHED]')



if __name__ == '__main__':
	SERVER.listen(MAX_CONNECTIONS)
	print('[STARTED] waiting for connection')
	ACCEPT_THREAD = Thread(target=wait_for_communication,args=(SERVER,))
	ACCEPT_THREAD.start()
	ACCEPT_THREAD.join()
	SERVER.close()
