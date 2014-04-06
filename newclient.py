__author__ = 'FuWei'
import socket               # Import socket module
import string
import time					# Import time module
import platform				# Import platform module to get our OS
import os
from _thread import *
import pickle
def p2p_get_request(rfc_num):
    s = socket.socket() # Create a socket object
#s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEDADDR, 1)
    host = socket.gethostname()  # Get local machine name
    port = 65055             # You need to modify this port number according to the client
    s.connect((host, port))
    rfc_num = "1"
    data = "GET RFC "+rfc_num+" P2P-CI/1.0"
    s.send(bytes(data, 'utf-8'))
    data_rec = s.recv(1024)
    print (data_rec.decode('utf-8'))
    current_path = os.getcwd()
    filename = "rfc"+rfc_num+".txt"
    OS = platform.system()
    if OS == "Windows":  # determine rfc path for two different system
        filename = current_path + "\\rfc\\" + filename
    else:
        filename = current_path + "/rfc/" + filename
    f = open(filename,'w')
    f.write(data_rec.decode('utf-8'))
    f.close()
    s.close()
p2p_get_request(str(1))
#test