import socket
import os
from dotenv import load_dotenv

load_dotenv()

# get the port from the environment variable
port = os.getenv("PORT")
url = os.getenv("URL")

print(f"Server is running on {url}:{port}")

#  server source address (local host) along with port
address = (url, int(port))

# creating socket object (AF_INET (address family): IPv4, SOCK_STREAM (socket type): TCP)
tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# binding the socket object to the address
tcp.bind(address)

# backlog server can handle : 5 connections
tcp.listen(5)

print("Server is running on port 8080")


