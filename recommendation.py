import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import random

######################################################
def get_title_from_index(df, index):
	return df[df.index == index]["vid_id"].values[0]

def get_index_from_videoID(df, vid_id):
    return df[df.vid_id == vid_id].index[0]


def combine_features(row): 
	try:
		return row['vid_title'] +" "+row['category']+" "+row["description"]+" "+row["tags"]
	except:
		print("Error:", row	)

##########################################################


def recommender_videos(mood, activity_pref, liked_videos):
    """

    Function that will return a video recommendation based on the mood of the user, the preferred categories and     previously liked videos. 

    Parameters:
    - mood: 1=Happy/content, 2=Tired, 3=Stressed/unhappy
    - activity_pref = List of the activities the person has liked (sports, meditation etc.)
    - liked_videos = previously liked videos (of all categories)

    Function will return a dictionary with the url of the recommended video. 

    """

    #user_id = user_id
    activity_pref = activity_pref  
    target_activity =  random.choice(activity_pref)  ##TODO now target is chosen randomely, maybe depending on                                                              hour or something else?

    #print(target_activity)
    mood = mood  
    liked_videos = liked_videos #previously liked videos
                                                                         

    df = pd.read_csv("df_content_v5.csv") #Loading content of all data of youtube dataframe
    

    filtered_df = df[df.sentiment_target == mood] #Filtering dataframe for sentiment and the target activity
    df = filtered_df[filtered_df.category == target_activity]
    df = df.reset_index() 

    liked_vid_of_category = []
    for elem in liked_videos: 
        if elem in df['vid_id'].values:
            liked_vid_of_category.append(elem)  #selecting the videos of liked_videos that are corresponding to                                                     the category/activity chosen. 
    vid_to_use = random.choice(liked_vid_of_category) #Select one video to use in the recommendation system.

    #print(vid_to_use)
    #return df

    #-----------------------------------------------------------------------------------------#
                                #part of recommending a video#

    ##Step 1: Select Features that are could be important
    features = ['vid_title','category','description','tags']

    #Step 2: Create a column in DF which combines all selected features
    for feature in features:
        df[feature] = df[feature].fillna('')
    
    df["combined_features"] = df.apply(combine_features,axis=1)

    #return df

    ##Step 3: Create count matrix from this new combined column
    cv = CountVectorizer()
    count_matrix = cv.fit_transform(df["combined_features"])

    #pca visualisation 
    
    ##Step 4: Compute the Cosine Similarity based on the count_matrix
    cosine_sim = cosine_similarity(count_matrix) 
    video_user_likes = vid_to_use
    
    ## Step 5: Get index of this movie from its title
    video = get_index_from_videoID(df, video_user_likes)
    #print(video)
    similar_videos =  list(enumerate(cosine_sim[video]))

    ## Step 6: Get a list of similar movies in descending order of similarity score
    sorted_similar_videos = sorted(similar_videos,key=lambda x:x[1],reverse=True)
    #sort_by_likes = sorted(sorted_similar_videos,key=lambda x:df["views"][x[0]],reverse=True) --> TODO Maybe               filter on likes or views as well?

    ## Step 7: Print titles of first 10 recommendations
    recommendations = []
    i=0
    for element in sorted_similar_videos:
        recommendations.append(get_title_from_index(df, element[0]))
        i += 1
        if i>10:
            break
    

    #Step 8: filter dataframe for recommended videos:
    df_recommended = df[df['vid_id'].isin(recommendations)]
    df_recommended = df_recommended[df_recommended.vid_id != video_user_likes] #eliminate any recommendation         that use already liked (thus watched) before.
    
    url_vid = df_recommended[["url"]].values[0][0] #getting the url of the first option. #TODO add more then 1 recommendation?

    
    url = {"url": url_vid} #Creating dctionary with url to return. 

    return url
