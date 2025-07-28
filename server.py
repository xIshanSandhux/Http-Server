import socket

#  server source address (local host) along with port
address = ("127.0.0.1", 8080)

# creating socket object
tcp  = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# binding the socket object to the address
tcp.bind(address)

# backlog server can handle : 5 connections
tcp.listen(5)

print("Server is running on port 8080")


