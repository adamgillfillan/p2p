#!/usr/bin/python           # This is client.py file

import socket               # Import socket module
import time					# Import time module
import platform				# Import platform module to get our OS
import os
import pickle
import random
from _thread import *
#test


def p2p_get_request(rfc_num, peer_host, peer_upload_port):
    s = socket.socket() # Create a socket object
    s.connect((peer_host, int(peer_upload_port)))
    data = p2p_request_message(rfc_num, host)
    s.send(bytes(data, 'utf-8'))
    data_rec= pickle.loads(s.recv(1024))
    print("Data_rec", str(data_rec))
    #my_data = data_rec.decode('utf-8')
    my_data = data_rec[1]
    print(my_data)
    current_path = os.getcwd()
    filename = "rfc"+rfc_num+".txt"
    OS = platform.system()
    if OS == "Windows":  # determine rfc path for two different system
        filename = current_path + "\\rfc\\" + filename
    else:
        filename = current_path + "/rfc/" + filename
    #f = open(filename,'w')
    with open(filename, 'w') as file:
        file.write(my_data)
    #f.write(data_rec.decode('utf-8'))
    #f.close()
    s.close()


# display p2p response message
def p2p_response_message(rfc_num): # the parameter "rfc_num" should be str
    filename = "rfc"+str(rfc_num)+".txt"
    current_time = time.strftime("%a, %d %b %Y %X %Z", time.localtime())
    OS = platform.system()
    m = filename.split()
    filename = "".join(m)
    current_path = os.getcwd()
    if OS == "Windows":  # determine rfc path for two different system
        filename = "rfc\\" + filename
    else:
        filename = "rfc/" + filename
    #print (current_path+"/"+filename)
    #print (os.path.exists(current_path+"/"+filename))
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
        message	= ["P2P-CI/1.0 "+ status + " "+ phrase + "\n"\
                  "Date: " + current_time + "\n"\
                  "OS: " + str(OS)+"\n"\
                  "Last-Modified: " + last_modified + "\n"\
                  "Content-Length: " + str(content_length) + "\n"\
                  "Content-Type: text/text \n", str(data)]
                  #+ str(data)

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
    return message


# display p2s request message for ADD method
def p2s_add_message(rfc_num, host, port, title):  # for ADD
    message = "ADD" + " RFC " + str(rfc_num)+" P2P-CI/1.0 \n"\
              "Host: " + str(host)+"\n"\
              "Port: " + str(port)+"\n"\
              "Title: " + str(title)+"\n"
    return [message, rfc_num, host, port, title]


# display p2s request message for LOOKUP method
def p2s_lookup_message(rfc_num, host, port, title, get_or_lookup):  # LOOKUP method
    message = "LOOKUP" + " RFC " + str(rfc_num)+" P2P-CI/1.0 \n"\
              "Host: " + str(host)+"\n"\
              "Port: " + str(port)+"\n"\
              "Title: " + str(title)+"\n"
    return [message, rfc_num, get_or_lookup]


#display p2s request message for LIST methods
def p2s_list_request(host, port):
    message = "LIST ALL P2P-CI/1.0 \n"\
              "Host: "+str(host)+"\n"\
              "Port: "+str(port)+"\n"
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



upload_port_num = 65000+random.randint(1, 500)  # generate a upload port randomly in 65000~65500
dict_list_of_rfcs = []  # list of dictionaries of RFC numbers and Titles.
s=socket.socket()          # Create a socket object
#s.setsockopt(socket.SOL_SOCKET, socket.SO_RESUEDADDR, 1)
#host = socket.gethostname()  # Get local machine name
host = "10.139.68.102"
port = 7734                  # Reserve a port for your service.
s.connect((host, port))
data = pickle.dumps(peer_information())  # send all the peer information to server
s.send(data)
data = s.recv(1024)
print(data.decode('utf-8'))
s.close


def print_combined_list(dictionary_list, keys):
    for item in dictionary_list:
        print(' '.join([item[key] for key in keys]))


def get_user_input():
    #if key press, then close:
    user_input = input("> Enter ADD, LIST, LOOKUP, GET, or EXIT:  ")
    if user_input == "EXIT":
        data = pickle.dumps("EXIT")
        #s.send(bytes('1', "utf-8"))
        s.send(data)
        s.close                     # Close the socket when done
    elif user_input == "ADD":
        user_input_rfc_number = input("> Enter the RFC Number: ")
        user_input_rfc_title = input("> Enter the RFC Title: ")

        data = pickle.dumps(p2s_add_message(user_input_rfc_number, host, upload_port_num, user_input_rfc_title))
        s.send(data)
        server_data = s.recv(1024)
        print(server_data.decode('utf-8'))
        get_user_input()
    elif user_input == "LIST":
        data = pickle.dumps(p2s_list_request(host, port))
        s.send(data)
        server_data = s.recv(1024)
        print(server_data.decode('utf-8'), end="")

        new_data = pickle.loads(s.recv(1024))
        print_combined_list(new_data[0], new_data[1])

        get_user_input()
    elif user_input == "GET":
        user_input_rfc_number = input("> Enter the RFC Number: ")
        user_input_rfc_title = input("> Enter the RFC Title: ")
        data = pickle.dumps(p2s_lookup_message(user_input_rfc_number, host, port, user_input_rfc_title, "0"))
        s.send(data)
        server_data = pickle.loads(s.recv(1024))
        print("SERVER DATA:", server_data)
        if not server_data[0]:
            print(server_data[1])
        else:
            p2p_get_request(str(user_input_rfc_number), server_data[0]["Hostname"], server_data[0]["Port Number"])
        get_user_input()
    elif user_input == "LOOKUP":
        user_input_rfc_number = input("> Enter the RFC Number: ")
        user_input_rfc_title = input("> Enter the RFC Title: ")
        data = pickle.dumps(p2s_lookup_message(user_input_rfc_number, host, port, user_input_rfc_title, "1"))
        #print(p2s_lookup_message(user_input_rfc_number, host, port, user_input_rfc_title))
        #print(data)
        s.send(data)
        server_data = pickle.loads(s.recv(1024))
        #print(server_data[0][3])
        #print(server_data[0][1])
        print(server_data[1], end="")
        keys = ['RFC Number', 'RFC Title', 'Hostname', 'Port Number']
        print_combined_list(server_data[0], keys)
        get_user_input()
    else:
        get_user_input()


def p2p_listen_thread(str, i):
    upload_socket = socket.socket()
    host = socket.gethostname()
    upload_socket.bind((host, upload_port_num))
    upload_socket.listen(5)
    while True:
        c, addr = upload_socket.accept()
        data_p2p_undecode = c.recv(1024)
        data_p2p = data_p2p_undecode.decode('utf-8')
        indexP = data_p2p.index('P')
        indexC = data_p2p.index('C')
        rfc_num = data_p2p[indexC+1:indexP-1]# get the rfc_number
        print (rfc_num)
        print ('Got connection from', addr)
        c.send(pickle.dumps(p2p_response_message(rfc_num)))
        c.close()

# First we create new thread to handle upload listening event
# and then process the user input event, it looks like to be parrallel
# it works!
start_new_thread(p2p_listen_thread, ("hello", 1))
get_user_input()



# this is the upload socket for requesting from peers
#
# upload_socket= socket.socket()
# host = socket.gethostname()
# port = upload_port_num
# upload_socket.bind((host, port))
# upload_socket.listen(5)
# input=[upload_socket,sys.stdin]
# print ("hdhd")
# def peer_thread(conn, addr):
# 	data = c.recv(1024)
# 	indexP = data.index('P')
# 	indexC = data.index('C')
# 	rfc_num = data[indexC+1:indexP-1]# get the rfc_number
# 	print (rfc_num)
# 	print ('Got connection from', addr)
# 	c.send(p2p_response_message(rfc_num))
# 	c.close()                # Close the connection
#
#
# while True:
#     c, addr = upload_socket.accept()
#     input.append(c)
#     print("hello")
#     while True:
#         readyInput,readyOutput,readyException=select.select(input,[],[])
#         for indata in readyInput:
#             if indata == c:
#                 data = c.recv(1024)
#                 indexP = data.index('P')
#                 indexC = data.index('C')
#                 rfc_num = data[indexC+1:indexP-1]# get the rfc_number
#                 print(rfc_num)
#                 print('Got connection from', addr)
#                 c.send(p2p_response_message(rfc_num))
#                 if not data:
#                     break
#             else:
#                 print("jj")
#                 get_user_input()
#     c.close()

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