#!/usr/bin/python           # This is client.py file

import socket               # Import socket module
import time					# Import time module
import platform				# Import platform module to get our OS
import os
import pickle
import select
import sys
from _thread import *
# def response_message(status):
# 	if(status == "200"):
# 		phrase = "OK"
# 	elif(status == "404"):
# 		phrase = "Not Found"
# 	elif(status == "400"):
# 		phrase = "Bad Request"
# 	elif(status == "502"):
# 		phrase = "P2P-CI Version Not Supported"	
# 	last_modified = time.ctime(os.path.getmtime(file))
# 	current_time = time.strftime("%a, %d %b %Y %X %Z", time.localtime())
# 	message="P2P-CI/1.0 "+ status + " "+ phrase + "\n"\
# 			"Date: "+ current_time + "\n"\
# 			"OS: "+str(OS)+"\n"


# display p2p response message
def p2p_response_message(rfc_num): # the parameter "rfc_num" should be str
    filename = "rfc"+str(rfc_num)+".txt"
    current_time = time.strftime("%a, %d %b %Y %X %Z", time.localtime())
    OS = platform.platform()
    if os.path.exists(filename) == 0:
        status = "404"
        phrase = "Not Found"
        message = "P2P-CI/1.0 "+ status + " "+ phrase + "\n"\
                    "Date:" + current_time + "\n"\
                    "OS: "+str(OS)+"\n"
    else:
        status = "200"
        phrase = "OK"
        txt = open(filename)
        data = txt.read()
        last_modified = time.ctime(os.path.getmtime(filename))
        content_length = os.path.getsize(filename)
        message	= "P2P-CI/1.0 "+ status + " "+ phrase + "\n"\
                  "Date: " + current_time + "\n"\
                  "OS: " + str(OS)+"\n"\
                  "Last-Modified: " + last_modified + "\n"\
                  "Content-Length: " + str(content_length) + "\n"\
                  "Content-Type: text/text \n"\
                  + str(data)
    #print message
    return message


# send rfcs to peers
def send_file(filename):  # send the RFC to peers
    txt = open(filename)
    data = txt.read(1024)
    while data:
        s.send(data)
        data = txt.read(1024)
    s.close()


# display p2p request message
def p2p_request_message(rfc_num, host):
    OS = platform.platform()
    message = "GET RFC "+str(rfc_num)+" P2P-CI/1.0 \n"\
              "Host: "+str(host)+"\n"\
              "OS: "+str(OS)+"\n"
    #print message
    return message


# display p2s request message for ADD method
def p2s_add_message(rfc_num, host, port, title):  # for ADD
    message = "ADD" + " RFC " + str(rfc_num)+" P2P-CI/1.0 \n"\
              "Host: " + str(host)+"\n"\
              "Port: " + str(port)+"\n"\
              "Title: " + str(title)+"\n"
    #print message
    return [message, rfc_num, host, port, title]


# display p2s request message for LOOKUP method
def p2s_lookup_message(rfc_num, host, port, title):  # LOOKUP method
    message = "LOOKUP" + " RFC " + str(rfc_num)+" P2P-CI/1.0 \n"\
              "Host: " + str(host)+"\n"\
              "Port: " + str(port)+"\n"\
              "Title: " + str(title)+"\n"
    #print message
    return message


#display p2s request message for LIST methods
def p2s_list_request(host, port):
    message = "LIST ALL P2P-CI/1.0 \n"\
              "Host: "+str(host)+"\n"\
              "Port: "+str(port)+"\n"
    #print message
    return message


#get the list of the local rfcs
def get_local_rfcs():
    rfcs_path = os.getcwd() + "/rfc"
    rfcs_num = [num[num.find("c")+1:num.find(".")] for num in os.listdir(rfcs_path) if 'rfc' in num]
    return rfcs_num


#pass peer's hostname, port number and rfc_num, rfc_title
def peer_information():
    keys = ["RFC Number", "RFC Title"]
    rfcs_num = get_local_rfcs()
    rfcs_title = get_local_rfcs()  # ["title1", "title2", "title3"] we use rfcs_num to fill in title
    for num, title in zip(rfcs_num, rfcs_title):
        entry = [num, title]
        dict_list_of_rfcs.insert(0, dict(zip(keys, entry)))
    return [upload_port_num, dict_list_of_rfcs]  # [port, rfcs_num, rfcs_title]



upload_port_num = 7777
dict_list_of_rfcs = []  # list of dictionaries of RFC numbers and Titles.
s=socket.socket()          # Create a socket object
#s.setsockopt(socket.SOL_SOCKET, socket.SO_RESUEDADDR, 1)
host = socket.gethostname()  # Get local machine name
port = 7734                  # Reserve a port for your service.
s.connect((host, port))
data = pickle.dumps(peer_information())  # send all the peer information to server
#print(data)
s.send(data)
data = s.recv(1024)
print(data.decode('utf-8'))
s.close


def get_user_input():
    #if key press, then close:

    user_input = input("> Enter 1 for exit: ")
    if user_input == "1":
        s.send(bytes('1', "utf-8"))
        s.close                     # Close the socket when done
    elif user_input == "2":
        user_input_rfc_number = input("> Enter the RFC Number: ")
        user_input_rfc_title = input("> Enter the RFC Title: ")

        data = pickle.dumps(p2s_add_message(user_input_rfc_number, host, upload_port_num, user_input_rfc_title))
        s.send(data)
        server_data = s.recv(1024)
        print(server_data.decode('utf-8'))
        get_user_input()
    else:
        get_user_input()



# this is the upload socket for requesting from peers

upload_socket= socket.socket() 
host = socket.gethostname()
port = upload_port_num
upload_socket.bind((host, port))
upload_socket.listen(5)
input=[upload_socket,sys.stdin] 

# def peer_thread(conn, addr):
# 	data = c.recv(1024)
# 	indexP = txt.index('P')
# 	indexC = txt.index('C')
# 	rfc_num = txt[indexC+1:indexP-1]# get the rfc_number 
# 	print (rfc_num)
# 	print ('Got connection from', addr)
# 	c.send(p2p_response_message(rfc_num))
# 	c.close()                # Close the connection
	
while True:
	c, addr = upload_socket.accept() 
	input.append(c)
	print("hello")
	while True:
		readyInput,readyOutput,readyException=select.select(input,[],[])
		for indata in readyInput:
			if indata == c:
				data = c.recv(1024)
				indexP = txt.index('P')
				indexC = txt.index('C')
				rfc_num = txt[indexC+1:indexP-1]# get the rfc_number 
				print (rfc_num)
				print ('Got connection from', addr)
				c.send(p2p_response_message(rfc_num))	
				if not data:
					break
			else:
				print ("jj")
				get_user_input()
	c.close()
				
	
	

# peers_information()

# p2s_list_request("wfu.eedu", "787")
# #p2s_request_message("234", "34", "wfu.ncsu.edu", "ADD", "This is a test")
# #p2p_response_message("2")
# s = socket.socket()         # Create a socket object
# host = socket.gethostname() # Get local machine name
# print host
# port = 38888               # Reserve a port for your service.
# #p2p_request_message(4434,host)
# s.connect((host, port))
# s.sendall(p2p_request_message("23444", "28888"))
# #s.sendall(p2p_response_message("234"))
# print s.recv(1024)
# s.close                     # Close the socket when done