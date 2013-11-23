from socket import *
from Crypto.Cipher import AES
import random
import default_data
import string
import time
from utils import *

#At the initialization time, the list of onion routers is available to
#it. It then decides an appropiate sequence of onion routers in order to transmit the message from
#the source to the destination. It distributes the keys to each of the routers. After this, network is
#set up. At the time of client to server communication, it encrypts the message whereas during server
#to client communication, it decrypts it and passes it to client.


class App_proxy:
	def __init__(self,selfAddr,router_list1):
		self.selfAddr=selfAddr
		self.sock=socket(AF_INET,SOCK_DGRAM)
		self.sock.bind(self.selfAddr)	
		data,self.clientAddr=self.sock.recvfrom(1024)
		self.destAddr=convert_message(data)[0]
		self.key_list=[]
		self.server_key=0
		self.router_list=router_list1
		random.shuffle(self.router_list)
		self.key_assign()

	def key_generate(self,size=16,chars=string.ascii_uppercase+string.digits):
		return ''.join(random.choice(chars) for x in range(size))
	
	def key_assign(self):
		for i in range(len(self.router_list)):
			self.key_list.append(self.key_generate())
		self.server_key=self.key_generate()
		
	def key_transfer(self):
		if len(self.router_list)>1:
			self.sock.sendto('_key_'+self.key_list[0]+'_nextip_'+str(self.router_list[1]),self.router_list[0])
		else:
			self.sock.sendto('_key_'+self.key_list[0]+'_nextip_'+str(self.destAddr),self.router_list[0])
		for i in range(1,len(self.router_list)):
			if i==len(self.router_list)-1:
				msg='_key_'+self.key_list[i]+'_nextip_'+str(self.destAddr)
			else:
				msg='_key_'+self.key_list[i]+'_nextip_'+str(self.router_list[i+1])
			for j in range(i-1,-1,-1):
				msg=encrypt_msg(self.key_list[j],msg)
			self.sock.sendto(msg,self.router_list[0])
		server_msg='_key_'+self.server_key+'_nextip_'+str(self.destAddr)
		for j in range(len(self.router_list)-1,-1,-1):
				server_msg=encrypt_msg(self.key_list[j],server_msg)
		self.sock.sendto(server_msg,self.router_list[0])

		
		
	def send_data(self,data):
		data=pad_string(data)
		data=encrypt_msg(self.server_key,data)
		for i in range(len(self.key_list)-1,-1,-1):
			data=encrypt_msg(self.key_list[i],data)
		self.sock.sendto(data,self.router_list[0])
			
	def decrypt_server_data(self,msg):
		for j in range(len(self.router_list)):
			msg=decrypt_msg(self.key_list[j],msg)
		msg=decrypt_msg(self.server_key,msg)
		return msg
	
	def recv_data(self):
		data,addr=self.sock.recvfrom(1024)
		if addr==self.clientAddr:
			print 'Data recieved from client :: ',data
			if data=='Disconnect':
				for i in range(len(self.router_list)):
					self.sock.sendto(data,self.router_list[i])
				self.sock.sendto(data,self.destAddr)
				return 0
			else:
				self.send_data(data)
				return 1
		else:
			msgaux=self.decrypt_server_data(data)
			msg=unpad_string(msgaux)
			print 'Data recieved from server :: ',msg
			self.sock.sendto(msg,self.clientAddr)
			return 1
			
	def close_connection(self):
		self.sock.close()	

		
if __name__=='__main__':
	c=App_proxy(('127.0.0.1',8500),default_data.router_list)
		
	inp=raw_input()
	if inp=='Connect':
		c.key_transfer()
	while True:
		if(c.recv_data()==0):
			break
	c.close_connection()
