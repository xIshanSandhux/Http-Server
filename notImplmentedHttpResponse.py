import logging
import os

def getNotImplmentedResponse():
    response = (    
         "HTTP/1.1 501 Not Implemented\r\n"
            "Content-Type: text/html; charset=utf-8\r\n"
            "\r\n"
            "<html><body><h1>501 Not Implemented</h1></body></html>"
        ).encode("utf-8")
    return response

def getHttpHeaders(fileType, length, httpVersion):
    return (
        f"{httpVersion} 501 Not Implemented\r\n"
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

def notImplmentedHttpResponse(path, contentType, httpVersion):
    # getting the http body
    httpBody = getHttpBody(path)
    # if the http body exists, then we can send the response
    if httpBody:
        response = getHttpHeaders(contentType,len(httpBody),httpVersion)+httpBody
        return response
    else:
        # if the http body does not exist, then sending a 501 response for 501 file
        return getNotImplmentedResponse()



