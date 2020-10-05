import os, sys
from flask import Flask, render_template, redirect, request, jsonify 
import time
import random
import json

root_path = os.path.dirname((os.path.dirname(__file__)))
sys.path.append(root_path)
print(sys.path)
from Utils.folders_tb import open_json

app = Flask(__name__)


@app.route("/")
def default():
    return "Hi, there :)"



@app.route('/get/dataframe', methods=['GET'])
def get(): 
    path = root_path + "\\Reto_tripulaciones\\data_users.json" 
    #direction to where json is saved.

    return open_json(path)
        


def main():
    
    print("STARTING PROCESS")
    print(os.path.dirname(__file__))
    

    settings_file = os.path.dirname(__file__) + "/settings.json"
    with open(settings_file, "r") as json_file_readed:
        json_readed = json.load(json_file_readed)

    SERVER_RUNNING = json_readed["server_running"]
    
    if SERVER_RUNNING:
        DEBUG = json_readed["debug"]
        HOST = json_readed["host"]
        PORT_NUM = json_readed["port"]
        app.run(debug=DEBUG, host=HOST, port=PORT_NUM)
    else:
        print("Server settings.json doesn't allow to start server. " + 
              "Please, allow it to run it.")
            
if __name__ == "__main__":
    main()