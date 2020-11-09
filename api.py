from flask import Flask, make_response, request, render_template
from recommendation import recommender_videos
import os

app = Flask(__name__)

@app.route("/")
def landing_page():
    return "Welcome to my api"


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


# configurar lo que va dentro de PORT es súper importante
app.run(host='0.0.0.0',port=os.getenv("PORT", 5000), debug=True)

