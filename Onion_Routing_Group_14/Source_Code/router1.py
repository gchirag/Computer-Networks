from socket import *
from Crypto.Cipher import AES
import string
from utils import *

#This is the code for intermediate path routers.
#In the initialisation part all the routers are given their kyer using onion routing key assignment then
#at that time they store their prev and next node address, which they use for further transmission till the user calls off

class Router:
	def __init__(self,selfAddr):
		self.selfAddr=selfAddr
		self.sock=socket(AF_INET,SOCK_DGRAM)
		self.sock.bind(self.selfAddr)
		data,addr=self.sock.recvfrom(1024)
		if data[0:5] == '_key_':
			self.prevAddr=addr
			self.key=data[5:].split('_nextip_')[0]
			self.nextAddr=convert_message(data[5:].split('_nextip_')[1])[0]

	def send_data(self,data,addr):
		self.sock.sendto(data,addr)
		print 'Data sent ::',data
	
	def recv_data(self):
		data,addr=self.sock.recvfrom(1024)
		if data=='Disconnect':
			return 0
		else:
			if addr==self.prevAddr:
				data_forward=decrypt_msg(self.key,data)
				print 'Data recieved from client :: ',data_forward
				self.send_data(data_forward,self.nextAddr)
			if addr==self.nextAddr:
				data_reverse=encrypt_msg(self.key,data)
				print 'Data recieved from server :: ',data_reverse
				self.send_data(data_reverse,self.prevAddr)
			return 1
		
	def close_connection(self):
		self.sock.close()
		
		
if __name__=='__main__':
	r=Router(('127.0.0.1',6000))
		
	while True:
		if(r.recv_data()==0):
			break
				
	r.close_connection()
