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

def httpHeaders(fileType, length, httpVersion, statusCode):
    if statusCode == 404:
        statusMessage = "Well Hard Luck Buddy"
    elif statusCode== 501:
        statusMessage = "Sorry Buddy feature not implemented"
    elif statusCode == 200:
        statusMessage = "Here you go Buddy"
    else:
        statusMessage = "Unknown Status Code"

    return (
        f"{httpVersion} {statusCode} {statusMessage}\r\n"
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
        return [httpBody, 200]
    else:
        logging.error(f"Path {path} does not exist")
        return [None, 404]

def httpResponse(path, contentType, httpVersion, requestType, isImplemented,pageNotFound):
    # getting the http body + checking if the file exists. if it does not exist then returning 404
    httpBody, statusCode = getHttpBody(path)
    # if the status code for the path and file is not 404, then updating the status code to the appropriate status code based on request
    if statusCode != 404:
        if not pageNotFound:
            if requestType == "GET" and isImplemented:
                statusCode = 200
            elif requestType == "POST" and isImplemented:
                statusCode = 201
            elif not isImplemented:
                statusCode = 501
        else:
            statusCode = 404
    else:
        # if the file does not exist then returning 404
        httpBody = getHttpBody("website/404.html")
    # if the http body exists, then we can send the response
    if httpBody:
        logging.debug(f"Sending response with status code {statusCode}")
        logging.debug(f"Sending response with content type {contentType}")
        logging.debug(f"Sending response with http version {httpVersion}")
        logging.debug(f"Sending response with length {len(httpBody)}")
        logging.debug(f"Sending response with http body {httpBody}")
        response = httpHeaders(contentType,len(httpBody),httpVersion,statusCode)+httpBody
        return response
    else:
        # if the http body does not exist, then sending a 404 response for 404 file
        return getNotFoundResponse()