import logging
import os

def getNotFoundResponse():
    response = (    
         "HTTP/1.1 404 Well Hard Luck Buddy\r\n"
            "Content-Type: text/html; charset=utf-8\r\n"
            "\r\n"
            "<html><body><h1>404 Well Hard Luck Buddy</h1></body></html>"
        ).encode("utf-8")
    return response

def getHttpHeaders(fileType, length, httpVersion):
    return (
        f"{httpVersion} 200 Here you go Buddy\r\n"
        f"Content-Type: {fileType}; charset=utf-8\r\n"
        f"Content-Length: {length}\r\n"
        "\r\n"
        ).encode("utf-8")

def getHttpBody(path):
    # checking if the path exists and is a file
    if os.path.exists(path) and os.path.isfile(path):
        # reading the file
        with open(path, "rb") as file:
            httpBody = file.read()
        return httpBody
    else:
        logging.error(f"Path {path} does not exist")
        return None

def getHttpResponse(path,contentType,httpVersion):
    # getting the http body
    httpBody = getHttpBody(path)
    # if the http body exists, then we can send the response
    if httpBody:
        response = getHttpHeaders(contentType,len(httpBody),httpVersion)+httpBody
        return response
    else:
        # if the http body does not exist, then sending a 404 response
        return getNotFoundResponse()



