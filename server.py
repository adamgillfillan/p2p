#!/usr/bin/python           # This is server.py file

import socket               # Import socket module
import time					# Import time module
import platform				# Import platform module to get our OS
from _thread import *
import pickle

s = socket.socket()# Create a socket object
host = socket.gethostname()  # Get local machine name
port = 7734                  # Reserve a port for your service.
s.bind((host, port))         # Bind to the port

s.listen(5)                  # Now wait for client connection.

peer_list = []  # Global list of dictionaries for peers
RFC_list = []   # Global list of dictionaries for RFCs
combined_list = []


def response_message(status):
    if status == "200":
        phrase = "OK"
    elif status == "404":
        phrase = "Not Found"
    elif status == "400":
        phrase = "Bad Request"
    message = "P2P-CI/1.0 " + status + " " + phrase + "\n"
    return message


# P2S response message from the server
def p2s_lookup_response(rfc_num): # the parameter "rfc_num" should be str
    current_time = time.strftime("%a, %d %b %Y %X %Z", time.localtime())
    OS = platform.platform()
    response = search_combined_dict(rfc_num)
    if not response:
        status = "404"
        phrase = "Not Found"
        message= "P2P-CI1111/1.0 "+ status + " "+ phrase + "\n"\
                 "Date: " + current_time + "\n"\
                 "OS: "+str(OS)+"\n"
        return response, message
    else:
        status = "200"
        phrase = "OK"
        message	= "P2P-CI11111/1.0 "+ status + " "+ phrase + "\n"
        return response, message


def p2s_lookup_response2(rfc_num): # the parameter "rfc_num" should be str
    current_time = time.strftime("%a, %d %b %Y %X %Z", time.localtime())
    OS = platform.platform()

    response = search_combined_dict2(rfc_num)
    if len(response) == 0:
        status = "404"
        phrase = "Not Found"
        message= "P2P-CI/1.0 "+ status + " "+ phrase + "\n"\
                 "Date: "+ current_time + "\n"\
                 "OS: "+str(OS)+"\n"
        return response, message
    else:
        status = "200"
        phrase = "OK"
        message	= "P2P-CI11111/1.0 "+ status + " "+ phrase + "\n"
        return response, message


def p2s_add_response(conn, rfc_num, rfc_title, hostname, port):
    response = "P2P-CI/1.0 200 OK \nRFC "+ rfc_num +" "+rfc_title+" "+str(hostname)+" "+str(port)
    conn.send(bytes(response, 'utf-8'))


def search_combined_dict(rfc_number):
    for d in combined_list:
        if d['RFC Number'] == rfc_number:
            return d

    return False


def search_combined_dict2(rfc_number):
    my_list = []
    for d in combined_list:
        if d['RFC Number'] == rfc_number:
            my_list.append(d)

    return my_list


def p2s_list_response(conn):
    message = response_message("200")
    #new_list = create_parsed_list_for_list_request()

    conn.send(bytes(message, 'utf-8'))


def send_file(filename):  # send the RFC to peers
    txt = open(filename)
    data = txt.read(1024)
    while data:
        s.send(data)
        data = txt.read(1024)
    s.close()


#Takes a list and appends a dictionary of hostname and port number
def create_peer_list(dictionary_list, hostname, port):
    keys = ['Hostname', 'Port Number']

    entry = [hostname, str(port)]
    dictionary_list.insert(0, dict(zip(keys, entry)))
    return dictionary_list, keys


#Creates RFC_list
def create_rfc_list(dictionary_list, dict_list_of_rfcs, hostname):
    keys = ['RFC Number', 'RFC Title', 'Hostname']

    for rfc in dict_list_of_rfcs:
        rfc_number = rfc['RFC Number']
        rfc_title = rfc['RFC Title']
        entry = [str(rfc_number), rfc_title, hostname]
        dictionary_list.insert(0, dict(zip(keys, entry)))

    return dictionary_list, keys


def create_combined_list(dictionary_list, dict_list_of_rfcs, hostname, port):
    keys = ['RFC Number', 'RFC Title', 'Hostname', 'Port Number']

    for rfc in dict_list_of_rfcs:
        rfc_number = rfc['RFC Number']
        rfc_title = rfc['RFC Title']
        entry = [str(rfc_number), rfc_title, hostname, str(port)]
        dictionary_list.insert(0, dict(zip(keys, entry)))

    return dictionary_list, keys


# Inserts new Dictionary item to RFC_list when client makes an ADD request
def append_to_rfc_list(dictionary_list, rfc_num, rfc_title, hostname):
    keys = ['RFC Number', 'RFC Title', 'Hostname']
    entry = [str(rfc_num), rfc_title, hostname]

    dictionary_list.insert(0, dict(zip(keys, entry)))
    return dictionary_list


def append_to_combined_list(dictionary_list, rfc_num, rfc_title, hostname, port):
    keys = ['RFC Number', 'RFC Title', 'Hostname', 'Port Number']
    entry = [str(rfc_num), rfc_title, hostname, str(port)]

    dictionary_list.insert(0, dict(zip(keys, entry)))
    return dictionary_list


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


def delete_combined_dictionary(combined_dict, hostname):
    combined_dict[:] = [d for d in combined_dict if d.get('Hostname') != hostname]
    return combined_dict


def return_dict():
    keys = ['RFC Number', 'RFC Title', 'Hostname', 'Port Number']
    return combined_list, keys


# Create a thread for each client. This prevents the server from blocking communication with multiple clients
def client_thread(conn, addr):
    global peer_list, RFC_list, combined_list
    conn.send(bytes('Thank you for connecting', 'utf-8'))
    print('Got connection from ', addr)
    data = pickle.loads(conn.recv(1024))  # receive the[upload_port_num, rfcs_num, rfcs_title]
    my_port = data[0]
    # Generate the peer list and RFC list
    peer_list, peer_keys = create_peer_list(peer_list, addr[0], data[0])  # change addr[1] to data[0]
    RFC_list, rfc_keys = create_rfc_list(RFC_list, data[1], addr[0])
    combined_list, combined_keys = create_combined_list(combined_list, data[1], addr[0], data[0])

    while True:
        data = pickle.loads(conn.recv(1024))  # receive the[upload_port_num, rfcs_num, rfcs_title]
        if data == "EXIT":
            break
        if type(data) == str:
            p2s_list_response(conn)
            new_data = pickle.dumps(return_dict())
            conn.send(new_data)
        else:
            if data[0][0] == "A":
                p2s_add_response(conn, data[1], data[4], addr[0], data[3])  # Put server response message here
                RFC_list = append_to_rfc_list(RFC_list, data[1], data[4], addr[0])
                combined_list = append_to_combined_list(combined_list, data[1], data[4], addr[0], my_port)
                print_dictionary(RFC_list, rfc_keys)
            if data[2] == "0":
                new_data = pickle.dumps(p2s_lookup_response(data[1]))
                conn.send(new_data)
            elif data[2] == "1":
                print(p2s_lookup_response2(data[1]))
                new_data = pickle.dumps(p2s_lookup_response2(data[1]))
                conn.send(new_data)

    # Remove the client's info from the dictionaries
    peer_list = delete_peers_dictionary(peer_list, addr[0])
    RFC_list = delete_rfcs_dictionary(RFC_list, addr[0])
    combined_list = delete_combined_dictionary(combined_list, addr[0])
    #print_dictionary(peer_list, peer_keys)
    #print_dictionary(RFC_list, rfc_keys)
    #print_dictionary(combined_list, combined_keys)
    conn.close()
while True:
    c, addr = s.accept()     # Establish connection with client.
    start_new_thread(client_thread, (c, addr))
s.close()