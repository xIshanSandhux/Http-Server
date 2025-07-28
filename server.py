import socket
import os
from dotenv import load_dotenv
import logging

load_dotenv()

# logging configuration
logging.basicConfig(format='%(levelname)s: %(message)s', level=logging.DEBUG)

# getting the port and url from the environment variable
try:
    port = os.getenv("PORT") 
    url = os.getenv("URL") 

    if not port or not url:
        logging.critical("Port or URL is not set")
        exit(1)
    logging.info(f"URL from env: {url} and Port from env: {port}")
except Exception as e:
    logging.error(f"Error: {e}")

#  server source address (local host) along with port
if port.isdigit():
    address = (url, int(port))
    logging.debug(f"Address: {address}")
else:
    logging.critical("Port is not an int therefore could not bind the socket")
    exit(1)

# creating socket object (AF_INET (address family): IPv4, SOCK_STREAM (socket type): TCP)
tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# SO_REUSEADDR allows the socket to be reused immediately after closing even if it is in a TIME_WAIT state
tcp.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

# binding the socket object to the address
tcp.bind(address)

# Max backlog that the server can handle: 5 connections
tcp.listen(5)

logging.info(f"HTTP Server is running on port: {port} and url: {url}")

try:
    while True:
        try:        
            # accepting a connection from the client
            conn, addr = tcp.accept()
            logging.debug(f"Connection: from IP and Port: {addr}")
            # reading the request from the client (decoding the data from bytes to string)
            data = conn.recv(4096).decode("utf-8")
            logging.debug(f"Data from client: {data}")

            # sending sample HTTP response
            response =(
                "HTTP/1.1 200 OK\r\n"
                "Content-Type: text/html\r\n"
                "\r\n"
                "<html><body><h1>Hello, World!</h1></body></html>"
            )

            # encoding the response to bytes
            http_response = response.encode("utf-8")

            # sending the response to the client
            conn.sendall(http_response)

        except Exception as e:
            logging.error(f"Error:{e}")
        
        finally:
            logging.info("Closing the connection")
            conn.close()
except KeyboardInterrupt:
    logging.info("Server is shutting down")
finally:
    tcp.close()
    exit(0)