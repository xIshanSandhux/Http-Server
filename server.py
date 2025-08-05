import socket
import os
from dotenv import load_dotenv
import logging
from httpResponse import httpResponse
from post import registeration, login

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
if port and port.isdigit():
    port = int(port)
    if 1<=port<=65535:
        address = (url, port)
    else:
        logging.critical("Port is not in the range of 1-65535")
        exit(1)
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
        conn = None
        try:        
            # accepting a connection from the client
            conn, addr = tcp.accept()
            logging.debug(f"Connection: from IP and Port: {addr}")
            conn.settimeout(10)

            try:
                # reading the request from the client (looping until the end of the request)
                headersBinary = b""
                while b"\r\n\r\n" not in headersBinary:
                    chunks = conn.recv(1024)
                    if not chunks:
                        break
                    headersBinary += chunks

                
                # decoding the request from bytes to string
                # splitting the request into headers and payload
                # splitting the headers into a list
                initialData = headersBinary.decode("utf-8")
                if not initialData:
                    logging.error("No data from client")
                    # ignoring the rest of the code for this connection
                    continue

                headers, payload = initialData.split("\r\n\r\n")
                headerList = headers.split("\r\n")

                logging.debug(f"Full Request: {headersBinary}")

                # logging the payload and the header list
                # logging.debug(f"Payload: {payload}")
                logging.debug(f"Header List: {headerList}")

                contentLength = 0
                contentType = ""
                boundary = ""
                for line in headerList:
                    if line.startswith("Content-Length"):
                        contentLength = int(line.split(" ")[1])
                        logging.debug(f"Content Length: {contentLength}")
                    elif line.startswith("Content-Type"):
                        contentType = line.split(" ")[1].strip(";")
                        if contentType == "multipart/form-data":
                            boundary = line.split(";")[1].split("=")[1]
                        logging.debug(f"Content Type: {contentType}")
                        logging.debug(f"Boundary: {boundary}")
                
                # -------------Content Type: multipart/form-data-------------------
                if contentType == "multipart/form-data" and boundary:
                    if contentLength>0:
                        binaryPayload = b""
                        while len(binaryPayload)<contentLength:
                            chunk = conn.recv(1024)
                            if not chunk:
                                break
                            binaryPayload += chunk
                        boundary = boundary.encode("utf-8")
                        listbinary = binaryPayload.split(b"--"+boundary)
                        logging.debug(f"LIST BINARY: {listbinary}")
                        for line in listbinary:
                            if b"name=\"username\"" in line:
                                usernameLine = line.decode("utf-8").split(" ")[2]
                                username = usernameLine.split("\r\n\r\n")[1].strip("\r\n")
                                logging.debug(f"Username: {username}")

                            elif b"name=\"password\"" in line:
                                passwordLine = line.decode("utf-8").split(" ")[2]
                                password = passwordLine.split("\r\n\r\n")[1].strip("\r\n")
                                logging.debug(f"Password: {password}")
                            elif b"name=\"email\"" in line:
                                emailLine = line.decode("utf-8").split(" ")[2]
                                email = emailLine.split("\r\n\r\n")[1].strip("\r\n")
                                logging.debug(f"Email: {email}")
                        fullPayload = payload[:contentLength]

                # -------------Content Type: multipart/form-data-------------------

                # ---------Content Type: application/x-www-form-urlencoded---------
                # if fullPayload and contentType == "application/x-www-form-urlencoded":
                #     items = fullPayload.split("&")
                #     logging.debug(f"Items: {items}")
                #     itemsDict = {}
                #     for item in items:
                #         key, value = item.split("=")
                #         if key not in itemsDict:
                #             itemsDict[key] = value
                #     logging.debug(f"Items based on key value pairs: {itemsDict}")
                # ---------Content Type: application/x-www-form-urlencoded---------

                # headerList = data.split("\r\n")
                # logging.debug(f"Header List: {headerList}")

                requestLine = headerList[0]
                logging.debug(f"Request Line: {requestLine}")

                requestComponents = requestLine.split(" ")
                logging.debug(f"Request Components: {requestComponents}")

                requestType = requestComponents[0]
                path = requestComponents[1]
                httpVersion = requestComponents[2]
                logging.debug(f"Request Type: {requestType} and Path: {path}")

                if requestType == "GET":
                    if path == "/":
                        response  = httpResponse("website/homepage.html", "text/html", httpVersion, requestType, True,False)
                    elif path == "/favicon.ico":
                        response = httpResponse("website/favicon.ico", "image/x-icon", httpVersion, requestType, True,False)
                    else:
                        logging.debug("404 page is being displayed")
                        requestType = "NOT_FOUND"
                        response = httpResponse("website/404.html", "text/html", httpVersion, requestType, True, True)
                
                elif requestType == "POST":
                    if path == "/register":
                        if registeration(itemsDict):
                            logging.debug("Registration successful")
                    elif path =="/login":
                        if login(itemsDict):
                            logging.debug("Login successful")
                        else:
                            logging.debug("Login failed")
                
                else:
                    logging.debug("501 page is being displayed")
                    response = httpResponse("website/501.html", "text/html", httpVersion, requestType, False,False)
                # sending the response to the client
                conn.sendall(response)
            except Exception as e:
                logging.error(f"Data could not be read from client:{e}")

        except socket.timeout as e:
            logging.error(f"Timeout:{e}")
        finally:
            if conn:
                logging.info("Closing the connection")
                conn.close()
except KeyboardInterrupt:
    logging.info("Server is shutting down")
finally:
    tcp.close()
    exit(0)