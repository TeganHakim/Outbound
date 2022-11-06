# Import libraries to access system files
import os

def getSubDir(client_surname):
    PATH = os.getcwd().replace("\src", "")
    for file in os.listdir(PATH + "\masters"):
        if client_surname == file:
            return "\masters\\"
    for file in os.listdir(PATH + "\clients"):
        if client_surname == file:
            return "\clients\\"
    return "\clients\\"