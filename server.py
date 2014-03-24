__author__ = 'Adam'
import socket
from _thread import *

s = socket.socket()          # Create a socket object
host = socket.gethostname()  # Get local machine name
port = 7734                  # Reserve a port for your service.
s.bind((host, port))         # Bind to the port

s.listen(5)                  # Now wait for client connection.

peer_list = []  # Global list of dictionaries for peers
RFC_list = []   # Global list of dictionaries for RFCs

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

    # Generate the peer list and RFC list
    peer_list, peer_keys = create_peer_list(peer_list, addr[0], addr[1])
    RFC_list, rfc_keys = create_rfc_list(RFC_list, example_dict_list_of_rfcs, addr[0])
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