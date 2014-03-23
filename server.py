__author__ = 'Adam'
import socket

s = socket.socket()         # Create a socket object
host = socket.gethostname() # Get local machine name
port = 7734                # Reserve a port for your service.
s.bind((host, port))        # Bind to the port

s.listen(5)                 # Now wait for client connection.

peer_list = []
RFC_list = []


#Takes a list and appends a dictionary of hostname and port number
def create_peer_list(dictionary_list, hostname, port):
    keys = ['Hostname', 'Port Number']

    entry = [hostname, str(port)]
    dictionary_list.insert(0, dict(zip(keys, entry)))
    return peer_list, keys

example_dict_list_of_rfcs = [{'RFC Number': 1234, 'RFC Title': "This is an RFC Title"},
                             {'RFC Number': 4321, 'RFC Title': "This is another RFC Title"}]


#Creates RFC_list
def create_rfc_list(dictionary_list, dict_list_of_rfcs, hostname):
    keys = ['RFC Number', 'RFC Title', 'Hostname']

    for rfc in dict_list_of_rfcs:
        rfc_number = rfc['RFC Number']
        rfc_title = rfc['RFC Title']
        entry = [rfc_number, rfc_title, hostname]
        dictionary_list.insert(0, dict(zip(keys, entry)))

    return RFC_list, keys


#Prints the list of dictionary items
def print_dictionary(dictionary_list, keys):
    for item in dictionary_list:
        print(' '.join([item[key] for key in keys]))


while True:
    c, addr = s.accept()     # Establish connection with client.
    print('Got connection from', addr)
    peer_list, keys = create_peer_list(peer_list, addr[0], addr[1])
    print_dictionary(peer_list, keys)
    c.send(bytes('Thank you for connecting', "utf-8"))
    c.close()                # Close the connection
