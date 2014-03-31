#!/usr/bin/python           # This is server.py file

import socket               # Import socket module
import string 
import time					# Import time module
import platform				# Import platform module to get our OS
import os
from _thread import *
import pickle

s = socket.socket()          # Create a socket object
host = socket.gethostname()  # Get local machine name
port = 7734                  # Reserve a port for your service.
s.bind((host, port))         # Bind to the port

s.listen(5)                  # Now wait for client connection.

peer_list = []  # Global list of dictionaries for peers
RFC_list = []   # Global list of dictionaries for RFCs

# s = socket.socket()         # Create a socket object
# host = socket.gethostname() # Get local machine name
# port = 38888            # Reserve a port for your service.
# s.bind((host, port))        # Bind to the port
# 
# s.listen(5)                 # Now wait for client connection.


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


# P2S response message from the server
def p2s_lookup_response(rfc_num): # the parameter "rfc_num" should be str
    filename = "rfc"+str(rfc_num)+".txt"
    current_time = time.strftime("%a, %d %b %Y %X %Z", time.localtime())
    OS = platform.platform()
    if(os.path.exists(filename)==0):
        status = "404"
        phrase = "Not Found"
        message= "P2P-CI/1.0 "+ status + " "+ phrase + "\n"\
                 "Date: "+ current_time + "\n"\
                 "OS: "+str(OS)+"\n"
    else:
        status = "200"
        phrase = "OK"
        txt = open(filename)
        data = txt.read()
        last_modified = time.ctime(os.path.getmtime(filename))
        content_length = os.path.getsize(filename)
        message	= "P2P-CI/1.0 "+ status + " "+ phrase + "\n"\
        		  + str(data)
        ##################
        #######need to discuss with adam about interface
        ###################
        #print message
    return message

def send_file(filename):  # send the RFC to peers
    txt = open(filename)
    data = txt.read(1024)
    while(data):
        s.send(data)
        data =txt.read(1024)
    s.close()

# Example list of dictionaries of RFC numbers and Titles.
example_dict_list_of_rfcs = [{'RFC Number': 1234, 'RFC Title': "This is an RFC Title"},
                             {'RFC Number': 4321, 'RFC Title': "This is another RFC Title"}]


#Takes a list and appends a dictionary of hostname and port number
def create_peer_list(dictionary_list, hostname, port):
    keys = ['Hostname', 'Port Number']

    entry = [hostname, str(port)]
    dictionary_list.insert(0, dict(zip(keys, entry)))
    return dictionary_list, keys


#Creates RFC_list
def create_rfc_list(dictionary_list, dict_list_of_rfcs, hostname):
    #global RFC_list
    keys = ['RFC Number', 'RFC Title', 'Hostname']

    for rfc in dict_list_of_rfcs:
        rfc_number = rfc['RFC Number']
        rfc_title = rfc['RFC Title']
        entry = [str(rfc_number), rfc_title, hostname]
        dictionary_list.insert(0, dict(zip(keys, entry)))

    return dictionary_list, keys


# Prints the list of dictionary items
def print_dictionary(dictionary_list, keys):
    for item in dictionary_list:
        print(' '.join([item[key] for key in keys]))


# Deletes the entries associated with the hostname
def delete_peers_dictionary(dict_list_of_peers, hostname):
    dict_list_of_peers[:] = [d for d in dict_list_of_peers if d.get('Hostname') != hostname]
    return dict_list_of_peers


# Deletes the entries associated with the hostname
def delete_rfcs_dictionary(dict_list_of_rfcs, hostname):
    dict_list_of_rfcs[:] = [d for d in dict_list_of_rfcs if d.get('Hostname') != hostname]
    return dict_list_of_rfcs


# Create a thread for each client. This prevents the server from blocking communication with multiple clients
def client_thread(conn, addr):
    global peer_list, RFC_list
    conn.send(bytes('Thank you for connecting', 'utf-8'))
    print('Got connection from', addr)
    data = pickle.loads(conn.recv(1024))  # receive the[upload_port_num, rfcs_num, rfcs_title]
    print (data)
    # Generate the peer list and RFC list
    peer_list, peer_keys = create_peer_list(peer_list, addr[0], data[0]) # change addr[1] to data[0]
    RFC_list, rfc_keys = create_rfc_list(RFC_list, data[1], addr[0])
    print_dictionary(peer_list, peer_keys)
    print_dictionary(RFC_list, rfc_keys)

    while True:
        #Receiving from client
        data = conn.recv(1024)
        data = data.decode("utf-8")
        if data == "1":
            break

    # Remove the client's info from the dictionaries
    peer_list = delete_peers_dictionary(peer_list, addr[0])
    RFC_list = delete_rfcs_dictionary(RFC_list, addr[0])
    print_dictionary(peer_list, peer_keys)
    print_dictionary(RFC_list, rfc_keys)

    conn.close()
while True:
    c, addr = s.accept()     # Establish connection with client.
    start_new_thread(client_thread, (c, addr))
s.close()

# while True:
#    c, addr = s.accept()     # Establish connection with client.
#    txt= c.recv(1024)
#    print txt
#    indexP = txt.index('P')
#    indexC = txt.index('C')
#    rfc_num = txt[indexC+1:indexP-1]# get the rfc_number 
#    print rfc_num
#    print 'Got connection from', addr
#    c.send(p2p_response_message(rfc_num))
#    c.close()                # Close the connection