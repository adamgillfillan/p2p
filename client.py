#!/usr/bin/python           # This is client.py file

import socket               # Import socket module
import time					# Import time module
import platform				# Import platform module to get our OS
import os
import pickle

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

upload_port_num = 7777
dict_list_of_rfcs = []  #list of dictionaries of RFC numbers and Titles.

# display p2p response message
def p2p_response_message(rfc_num): # the parameter "rfc_num" should be str
    filename = "rfc"+str(rfc_num)+".txt"
    current_time = time.strftime("%a, %d %b %Y %X %Z", time.localtime())
    OS = platform.platform()
    if(os.path.exists(filename) == 0):
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
                  "Date: "+ current_time + "\n"\
                    "OS: "+str(OS)+"\n"\
                  "Last-Modified: " + last_modified + "\n"\
                  "Content-Length: " + str(content_length) + "\n"\
                  "Content-Type: text/text \n"\
                   +str(data)
    #print message
    return message

# send rfcs to peers
def send_file(filename):  # send the RFC to peers
    

    txt = open(filename)
    data = txt.read(1024)
    while(data):
        s.send(data)
        data =txt.read(1024)
    s.close()

# display p2p request message
def p2p_request_message(rfc_num, host):
	OS = platform.platform()
	message = "GET RFC "+str(rfc_num)+" P2P-CI/1.0 \n"\
		      "Host: "+str(host)+"\n"\
		      "OS: "+str(OS)+"\n"
	#print message
	return message

# display p2s request message for ADD and LOOKUP methods
def p2s_request_message(rfc_num, host, port, method, title):# for ADD, LOOKUP method
	message = method + " RFC " +str(rfc_num)+" P2P-CI/1.0 \n"\
			  "Host: "+str(host)+"\n"\
			  "Port: "+str(port)+"\n"\
			  "Title: "+str(title)+"\n"
	#print message
	#return message


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
	rfcs_num =[num[num.find("c")+1:num.find(".")] for num in os.listdir(rfcs_path) if 'rfc' in num]
	return rfcs_num

#pass peer's hostname, port number and rfc_num, rfc_title

def peer_infomation():
	keys = ["RFC Number", "RFC Title"]
	rfcs_num = get_local_rfcs()
	rfcs_title = ["title1", "title2", "title3"]
	for num, title in zip(rfcs_num, rfcs_title):
		entry = [num, title]
		dict_list_of_rfcs.insert(0, dict(zip(keys, entry)))
	return [upload_port_num, dict_list_of_rfcs]  #[port, rfcs_num, rfcs_title]


s=socket.socket()          # Create a socket object
host = socket.gethostname()  # Get local machine name
port = 7734                  # Reserve a port for your service.

s.connect((host, port))
data = pickle.dumps(peer_infomation())
print (data)
s.send(data)
data = s.recv(1024)
print(data.decode('utf-8'))



#if key press, then close:
user_input = input("> Enter 1 for exit: ")
if user_input == "1":
    s.send(bytes('1', "utf-8"))
    s.close                     # Close the socket when done
elif user_input == "2":
     pass

else:
    user_input = input("> Enter 1 for exit: ")




# peers_infomation()

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