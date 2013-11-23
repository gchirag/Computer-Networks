from socket import *
from threading import Thread

#This is client's code and its completely naive about the protocol of onion routing.
#It intially sends destination address to Application proxy and begins the conversation thereafter.

DESTNADDR = ('127.0.0.1',9000)
APPNPROXY = ('127.0.0.1',8500)
SELFADDR = ('127.0.0.1',8000)

class Client:
	def __init__(self,selfAddr,destAddr):
		self.selfAddr=selfAddr
		self.destAddr=destAddr
		self.sock=socket(AF_INET,SOCK_DGRAM)
		self.sock.bind(self.selfAddr)
		self.sock.settimeout(10)
	
	def send_data(self,data):
		self.sock.sendto(data,self.destAddr)
		print 'Data sent to server::',data

	def recv_data(self,inp):
		while True:
			try:
				data,addr=self.sock.recvfrom(1024)
				break
			except timeout:
				print "Ack not received...sending again"
				self.send_data(inp)
		print 'Data recieved from server :: ',data
	
	def close_connection(self):
		self.sock.close()
		
		
if __name__=='__main__':
	c=Client(SELFADDR,APPNPROXY)
	inp=str(DESTNADDR)
	c.send_data(inp)

	while True:
		inp=raw_input()
		c.send_data(inp)
		if(inp=='Disconnect'):
			print 'Disconnected'
			break
		else:
			c.recv_data(inp)
		
	c.close_connection()
