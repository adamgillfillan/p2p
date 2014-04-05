__author__ = 'FuWei'
import socket               # Import socket module
import string
import time					# Import time module
import platform				# Import platform module to get our OS
import os
from _thread import *
import pickle

s = socket.socket()# Create a socket object
#s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEDADDR, 1)
host = socket.gethostname()  # Get local machine name
port = 65283                # You need to modify this port number according to the client
s.connect((host,port))
data = "GET RFC 1 P2P-CI/1.0"
s.send(bytes(data, 'utf-8'))
data_rec = s.recv(1024)
print (data_rec.decode('utf-8'))
s.close()