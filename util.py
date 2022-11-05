# Import libraries to access system files
import os

def getSubDir(client_surname):
        for file in os.listdir(os.getcwd() + "/masters"):
            if client_surname == file:
                return "/masters/"
        for file in os.listdir(os.getcwd() + "/clients"):
            if client_surname == file:
                return "/clients/"
        return "/clients/"