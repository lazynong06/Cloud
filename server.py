#coding:utf-8
import socket
import time
import datetime
import threading

ANY = '0.0.0.0'
SENDERPORT=2000 #SENDERPORT can be modified but there is no nessasity to do that...
MCAST_ADDR = '224.168.4.16'
MCAST_PORT = 4000

message_history = []


def sender(nickname, group_addr, group_port):
	sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP) 
	sock.bind((ANY,SENDERPORT)) #bind senderport to 2000
	sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 255) #using multicast
	print "Input '+new message' to send new message or input '-n' to pull latest n messages in the group."
	while 1:
		tosend = raw_input("#")
		if len(tosend)>0:
			if tosend[0]=='+':
    				sock.sendto(nickname + tosend, (MCAST_ADDR,MCAST_PORT) ); #send message to multicast port 4000
			elif tosend[0]=='-':
				try:
					n = int(tosend[1:])
				except:
					print "Invalid input!"
				else:
					n = min(n,len(message_history)) #in case that n is bigger than number of messages
					for i in range(len(message_history)-n, len(message_history)):
						nc = message_history[i][0].split('+',1)
						print nc[0] + '('+message_history[i][1]+') ' +message_history[i][2]+'\n'
						print nc[1]+'\n'
			else:
				print "no '-' or '+' in prefix, check your input!"
		else:
			pass
				


def receiver(args):
	sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
	sock.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1) 
	sock.bind((ANY,MCAST_PORT)) #bind port
	sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 255) # tell kernel this is a multicast
	status = sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, socket.inet_aton(MCAST_ADDR) + socket.inet_aton(ANY));

	sock.setblocking(0)
	ts = time.time()
	while 1: 
		try: 
    	    		data, addr = sock.recvfrom(1024) 
    		except socket.error, e: 
    	   		pass 
    		else:
			now = datetime.datetime.now()
    	    		message_history.append((data,addr[0],now.strftime("%Y-%m-%d %H:%M:%S")))


def main():
	print "Thank you for using my software, and I hope you will enjoy it!"
	name = raw_input("What is your name?\n")
	addr = raw_input("Which group do you want to join? You should tell me the multicast ip address.\n")
	port = raw_input("And the port of the group?\n")
	
	receiver_thread = threading.Thread(target=receiver, args=(1,),name='receiver')
	sender_thread = threading.Thread(target=sender, args=(name,addr,port),name='sender')
	receiver_thread.start()
	sender_thread.start()

main()
