import logging
import urllib.parse

users = {}

def registeration(itemsDict: dict) -> bool:
    if "username" in itemsDict and "password" in itemsDict and "email" in itemsDict:
        email = urllib.parse.unquote(itemsDict["email"])
        password = urllib.parse.unquote(itemsDict["password"])
        username = urllib.parse.unquote(itemsDict["username"])
        users[email] = {"username": username, "password": password}
        logging.info(f"TotalUsers: {users}")
        return True
    else:
        return False

def login(itemsDict: dict) -> bool:
    if "email" in itemsDict and "password" in itemsDict:
        email = urllib.parse.unquote(itemsDict["email"])
        password = urllib.parse.unquote(itemsDict["password"])
        if email not in users:
            return False
        if users[email]["password"] == password:
            return True
        else: 
            return False