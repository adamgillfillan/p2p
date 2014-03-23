__author__ = 'Adam'
#!/usr/bin/python            # This is client.py file

import socket                # Import socket module

s = socket.socket()          # Create a socket object
host = socket.gethostname()  # Get local machine name
port = 7734                  # Reserve a port for your service.

s.connect((host, port))
data = s.recv(1024)
print(data.decode('utf-8'))
#if key press, then close:
user_input = input("> Enter 1 for exit: ")
if user_input == "1":
    s.send(bytes('1', "utf-8"))
    s.close                     # Close the socket when done
else:
    user_input = input("> Enter 1 for exit: ")