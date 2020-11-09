import os, sys
from flask import Flask, render_template, redirect, request, jsonify 
import time
import random
import json
from recommendation import recommender_videos

root_path = os.path.dirname((os.path.dirname(__file__)))
sys.path.append(root_path)
print(sys.path)
from Utils.folders_tb import open_json

app = Flask(__name__)


@app.route("/")
def default():
    return "Hi, there :)"



@app.route('/get/recommendation', methods=['GET'])
def get(): 
    
  

    if 'mood' in request.args:
        mood = int(request.args['mood'])
    else: 
        return "This is a message of error: Missing argument: mood"
    if 'activity_pref' in request.args.to_dict(flat=False):   
        pref = []
        for elem in (request.args.to_dict(flat=False)['activity_pref']):
            pref.append(str(elem))
    else: 
        return "This is a message of error: Missing argument: activity_pref"

    if 'liked_videos' in request.args:
        liked_vid = []
        for elem in (request.args.to_dict(flat=False)['liked_videos']):
            liked_vid.append(str(elem))

    else: 
        
        return "This is a message of error: Missing argument: liked_videos"

    vid = recommender_videos(mood=mood, activity_pref=pref, liked_videos=liked_vid)

    return vid
         


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