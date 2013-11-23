from Crypto.Cipher import AES
import string

#This files contains some common functions which are frequently used in other files.
#This utility file is to be imported in each code.

def convert_message(message):
	temp = message.partition('(')[2]
	temp1 = temp.partition(',')[0]
	temp2 = temp.partition(',')[2]
	ip = temp1.split("'")[1]
	port = string.atoi(temp2.partition(')')[0])
	data = temp2.partition(')')[2]
	return ((ip,port),data)
	
def encrypt_msg(key,message):
	encryptor =AES.new(key,AES.MODE_CBC)
	return encryptor.encrypt(message)

def decrypt_msg(key,message):
	decryptor =AES.new(key,AES.MODE_CBC)
	return decryptor.decrypt(message)
	
#Since AES standard requires strings to be in multiples of size 16, 
#that's why we need to pad  and unpad the message strings as when required.

def pad_string(data):
	if len(data)%16!=0:
		data=data+'$'*(16-len(data)%16)			#this is because AES encryptor requires message of length which is a multiple of 16
	return data
	
def unpad_string(data):
	data=data.partition('$')[0]
	return data
